from __future__ import annotations
from collections import Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any, List
import os

import cerberus  # type: ignore[import]
import toml


SPEC = {
    'general': {
        'type': 'dict',
        'schema': {
            'projects_root': {'type': 'string'},
            'projects_root_internal': {'type': 'string'},
            'hostname': {'type': 'string'},
            'schema_file_name': {'type': 'string'},
        }
    },

    'docker': {
        'type': 'dict',
        'schema': {
            'server_image': {'type': 'string'},
            'server_container': {'type': 'string'},
            'base_image': {'type': 'string'},
            'default_build_tag': {'type': 'string'},
        }
    },

    'autoconf': {
        'type': 'dict',
        'schema': {
            'vhost_directory': {'type': 'string'},
            'reload_command': {'type': 'string'},
        }
    },

    'cli': {
        'type': 'dict',
        'schema': {
            'debug': {
                'type': 'boolean',
            }
        }
    },

    'php': {
        'type': 'dict',
        'schema': {
            'default_version': {'type': 'string'},
            'versions': {
                'type': 'dict',
                'allow_unknown': True,
                'schema': {},
            }
        }
    },
}


class ConfigError(Exception): pass


@dataclass
class GeneralConfig(object):
    projects_root: str
    projects_root_internal: str
    hostname: str
    schema_file_name: str

    def __post_init__(self) -> None:
        d = os.path.expanduser(self.projects_root)
        d = os.path.normpath(d)
        self.projects_root = d


@dataclass
class DockerConfig(object):
    server_container: str
    server_image: str
    base_image: str
    default_build_tag: str


@dataclass
class AutoconfConfig(object):
    vhost_directory: str
    reload_command: str


@dataclass
class CLIConfig(object):
    debug: bool


@dataclass
class PHPVersionConfig(object):
    socket: str
    binary: str


@dataclass
class PHPConfig(object):
    default_version: str
    versions: MutableMapping[str, PHPVersionConfig]

    def __post_init__(self) -> None:
        for k, v in self.versions.items():
            if isinstance(v, Mapping):
                self.versions[k] = PHPVersionConfig(**v)


class Config(object):
    @staticmethod
    def load_dir(d: str = '/etc/devbox/host') -> Config:
        defaults_file = os.path.join(d, 'defaults.toml')
        local_file = os.path.join(d, 'local.toml')

        data = toml.load(defaults_file)

        if os.path.exists(local_file):
            local_data = toml.load(local_file)
            deep_merge(data, local_data)

        v = cerberus.Validator()
        v.validate(data, SPEC)
        if v.errors:
            raise ConfigError(v.errors)

        return Config(data)

    general: GeneralConfig
    autoconf: AutoconfConfig
    cli: CLIConfig
    php: PHPConfig

    def __init__(self, data: Mapping) -> None:
        self.general = GeneralConfig(**data['general'])
        self.docker = DockerConfig(**data['docker'])
        self.autoconf = AutoconfConfig(**data['autoconf'])
        self.cli = CLIConfig(**data['cli'])
        self.php = PHPConfig(**data['php'])


def deep_merge(dest: MutableMapping, src: Mapping) -> MutableMapping:
    """
    Merge two mappings (e.g. dicts) recursively
    
    Keys in `src` will override existing keys in `dest` like with dict.update,
    but mappings from `src` will be merged with existing mappings in `dest` at
    any depth.

    Returns `dest`.
    """
    for k, v in src.items():
        if isinstance(v, Mapping):
            dest[k] = deep_merge(dest.get(k, {}), v)
        else:
            dest[k] = v
    return dest