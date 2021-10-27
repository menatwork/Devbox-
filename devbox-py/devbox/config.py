import cerberus
import yaml


SPEC = {
    'general': {
        'type': 'dict',
        'schema': {
            'projects_root': {'type': 'string'},
            'schema_file': {'type': 'string'},
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

    'autoconf': {
        'type': 'dict',
        'schema': {
            'apache2': {
                'type': 'dict',
                'schema': {
                    'vhost_template': {'type': 'string'},
                    'vhost_directory': {'type': 'string'},
                    'reload_command': {'type': 'string'},
                }
            }
        }
    }
}


class ConfigError(Exception):
    pass


class Config(object):
    @staticmethod
    def load(file_path='/etc/devbox/config.yml'):
        with open(file_path) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        v = cerberus.Validator()
        v.validate(data, SPEC)

        if v.errors:
            raise ConfigError(v.errors)

        return Config(data)

    def __init__(self, data: dict):
        self.data = data

    def get(self, *path: 'list[str]', default=None):
        v = self.data

        for part in path[:-1]:
            try:
                v = v[part]
            except KeyError:
                full_path = '.'.join(path)
                raise ConfigError(f"while fetching {full_path}: no such key: {part}")

        v = v.get(path[-1], default)
        return v

    def require(self, *path: 'list[str]'):
        v = self.get(*path, default=ConfigError)
        if v is ConfigError:
            key = '.'.join(path)
            raise ConfigError(f"required key '{key}' missing")
        return v
