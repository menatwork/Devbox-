"""
Devbox schema files (.devbox.yml)
"""
from dataclasses import dataclass
from typing import Optional
import os
import pprint
import yaml

import cerberus  # type: ignore[import]

from .rules import SCHEMA_FILE_RULES


class SchemaError(Exception): pass


class SchemaNotFound(SchemaError): pass


class InvalidSchema(SchemaError):
    errors: dict
    file_path: Optional[str]

    def __init__(self, errors: dict, file_path: Optional[str] = None) -> None:
        super().__init__(self)
        self.errors = errors
        self.file_path = file_path

    def __str__(self) -> str:
        pretty_errors = pprint.pformat(self.errors)
        return f"{self.file_path}: invalid schema: {pretty_errors}"


@dataclass
class Project(object):
    type: Optional[str] = None
    webroot: Optional[str] = None
    php: Optional[str] = None
    resources: Optional['list[str]'] = None

    def __post_init__(self) -> None:
        self._sanitize_unquoted_php_version()

    def _sanitize_unquoted_php_version(self) -> None:
        if type(self.php) == float:
            self.php = str(self.php)


@dataclass
class InstanceSecureShell(object):
    host: str
    user: str


@dataclass
class InstanceDeployment(object):
    method: str
    dir: str


class Instance(object):
    ssh: InstanceSecureShell
    deployment: InstanceDeployment

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.ssh = InstanceSecureShell(**data['ssh'])
        self.deployment = InstanceDeployment(**data['deployment'])


class Schema(object):
    @staticmethod
    def load_file(file_path: str) -> 'Schema':
        """
        Load a `Schema` object from a file

        May raise `InvalidSchema` or `SchemaNotFound`.
        """
        try:
            with open(file_path) as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
        except yaml.YAMLError as e:
            raise SchemaError(f"Couldn't parse schema file {file_path}: {e}")

        return Schema(data, file_path)

    @staticmethod
    def find_and_load(boundary: str) -> 'Schema':
        """
        Automatically find and load a schema file

        First tries to find a schema file in the current working directory, then
        every parent directory until either `boundary` is reached, or the parent
        directory is '/'.

        May raise `InvalidSchema` or `SchemaNotFound`.
        """
        d = os.getcwd()

        if d != boundary and not d.startswith(boundary):
            raise ValueError(f"boundary ({boundary}) is outside of cwd ({d})")

        while d.startswith(boundary):
            schema_file = os.path.join(d, '.devbox.yml')

            if os.path.isfile(schema_file) or os.path.islink(schema_file):
                return Schema.load_file(schema_file)

            if d == '/':
                break

            d = os.path.dirname(d)

        raise SchemaNotFound()

    # metadata
    file_path: Optional[str]
    project_directory: Optional[str]
    project_name: Optional[str]

    # schema fields
    version: str
    project: Project
    instances: Optional['dict[str, Instance]']

    def __init__(self, data: dict, file_path: Optional[str] = None) -> None:
        super().__init__()

        self.validate(data, file_path)

        self.init_metadata(file_path)
        self.init_schema_fields(data)

    def validate(self, data: dict, file_path: Optional[str] = None) -> None:
        v = cerberus.Validator(allow_unknown=True)
        v.validate(data, SCHEMA_FILE_RULES)
        if v.errors:
            raise InvalidSchema(v.errors, file_path)

    def init_metadata(self, file_path: Optional[str] = None) -> None:
        self.file_path = file_path
        if file_path:
            pd = os.path.dirname(file_path)
            pd = os.path.abspath(pd)
            pn = os.path.basename(pd)

            self.project_directory = pd
            self.project_name = pn

    def init_schema_fields(self, data: dict) -> None:
        self.version = data['version']

        self.project = Project(**data['project'])

        if instances := data.get('instances'):
            self.instances = {}
            for (name, inst) in instances.items():
                self.instances[name] = Instance(inst)