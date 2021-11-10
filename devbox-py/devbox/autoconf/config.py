from configparser import ConfigParser


class Config(object):
    def __init__(self, config_file: str) -> None:
        parser = ConfigParser()
        with open(config_file) as f:
            parser.read_file(f)

        general = parser['general']
        self.projects_root = general['projects_root']
        self.schema_file = general['schema_file']

        apache2 = parser['apache2']
        self.apache2_vhost_template = apache2['vhost_template']
        self.apache2_vhost_directory = apache2['vhost_directory']
        self.apache2_reload_command = apache2['reload_command']

        php = parser['php']
        self.php_default_version = php['default_version']

        self.php_versions = parser['php.versions']
