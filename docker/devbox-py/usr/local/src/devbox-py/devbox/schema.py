import cerberus
import os
import yaml


class SchemaError(Exception):
    pass


class SchemaNotFound(SchemaError):
    pass


class Schema(object):
    # note: cerberus calls this "spec" a "schema" as well, but we'll refer to it
    # as a spec to avoid confusion with our schema files (.devbox.yml)
    SPEC = {
        'version': { 'type': 'integer' },

        'project': {
            'type': 'dict',
            'schema': {
                'type': { 'type': 'string' },
                'webroot': { 'type': 'string' },
                'php': { 'type': ['string', 'integer', 'float'] },
            }
        }
    }

    @staticmethod
    def find_and_load(boundary: str):
        d = os.getcwd()

        if d != boundary and not d.startswith(boundary):
            raise ValueError(f"boundary ({boundary}) is outside of cwd ({d})")

        while d.startswith(boundary):
            schema_file = os.path.join(d, '.devbox.yml')

            if os.path.isfile(schema_file) or os.path.islink(schema_file):
                return Schema(schema_file)

            if d == '/':
                break

            d = os.path.dirname(d)

        raise SchemaNotFound()

    def __init__(self, path: str):
        try:
            with open(path) as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
        except yaml.YAMLError as e:
            raise SchemaError(f"Schema file isn't valid YAML: {e}")

        v = cerberus.Validator(allow_unknown=True)
        v.validate(data, self.SPEC)
        if v.errors:
            raise SchemaError(f"Invalid schema file: {v.errors}")

        self.path = path
        self.project_dir = os.path.dirname(path)
        self.name = os.path.basename(self.project_dir)

        self.version = data.get('version')
        project = data.get('project', {})

        self.project_type = project.get('type')
        self.project_webroot = project.get('webroot')
        self.project_php_version = sanitize_php_version(project.get('php'))

    def vhost_file_path(self, vhost_dir: str) -> str:
        return os.path.join(vhost_dir, f'{self.name}.conf')


def sanitize_php_version(v):
    # handle unquoted version numbers in schema file
    if type(v) == int or type(v) == float:
        v = str(v)
    return v
