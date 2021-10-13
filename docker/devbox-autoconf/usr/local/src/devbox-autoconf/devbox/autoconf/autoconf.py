import logging
import os

from .config import Config
from .schema import Schema, SchemaError
from .watcher import SchemaFileWatcher


class Autoconf(object):
    """
    Main application object
    """
    def __init__(self, config_file):
        self.cfg = Config(config_file)

    def watch_and_update_vhosts(self):
        """
        The daemon's main loop, which ingests schema file events from
        `SchemaWatcher` and triggers VHost reconfigurations.
        """
        schemas_by_project_dir = {}
        default_php_version = self.cfg.php_default_version

        for event in SchemaFileWatcher(self.cfg.projects_root, self.cfg.schema_file):
            if event.is_new_or_changed():
                try:
                    schema_file_path = event.schema_file_path()

                    schema = Schema(schema_file_path, default_php_version)
                    schemas_by_project_dir[event.project_dir] = schema

                    logging.info(f"{schema.name}: updating vhost config")
                    self.vhost_update(schema)
                except SchemaError as e:
                    logging.error(f"{schema_file_path}: {e}")
                except Exception as e:
                    logging.error("Unexpected exception:")
                    logging.exception(e)

            elif event.is_gone():
                try:
                    schema = schemas_by_project_dir.pop(event.project_dir)
                    logging.info(f"{schema.name}: dropping vhost config")
                    self.vhost_drop(schema)
                except KeyError:
                    # unrelated directory or file deletion
                    pass

            else:
                logging.warn(f"ignoring unknown watcher event: {event}")

    def vhost_update(self, schema: Schema):
        vhost_file = schema.vhost_file_path(self.cfg.apache2_vhost_directory)
        apache2_config = schema.to_apache2_vhost_config(self.cfg.php_versions)

        with open(vhost_file, 'w') as f:
            f.write(apache2_config)

        self.reload_apache2()

    def vhost_drop(self, schema: Schema):
        vhost_file = schema.vhost_file_path(self.cfg.apache2_vhost_directory)
        os.unlink(vhost_file)

        self.reload_apache2()

    def reload_apache2(self):
        cmd = self.cfg.apache2_reload_command
        r = os.system(cmd)
        if r != 0:
            logging.error(f"command returned {r}: {cmd}")
