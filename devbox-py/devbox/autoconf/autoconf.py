import logging
import os

import jinja2

from ..schema import Schema, SchemaError
from ..config import Config
from .watcher import SchemaFileWatcher


class Autoconf(object):
    """
    Main application object
    """
    def __init__(self):
        self.cfg = Config.load()

    def watch_and_update_vhosts(self):
        """
        The daemon's main loop, which ingests schema file events from
        `SchemaWatcher` and triggers VHost reconfigurations.
        """
        projects_root = self.cfg.get('general', 'projects_root')
        schema_file = self.cfg.get('general', 'schema_file')

        schemas_by_project_dir = {}

        for event in SchemaFileWatcher(projects_root, schema_file):
            if event.is_new_or_changed():
                try:
                    schema_file_path = event.schema_file_path()

                    schema = Schema(schema_file_path)
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
        try:
            apache2_config = self.render_apache2_vhost_config(schema)
        except IOError as e:
            logging.error(f"vhost update failed, couldn't read template: {e}")
            return
        except jinja2.TemplateError as e:
            logging.error(f"vhost update failed, invalid template: {e}")
            return

        try:
            vhost_dir = self.cfg.require('autoconf', 'apache2', 'vhost_directory')
            vhost_file = schema.vhost_file_path(vhost_dir)
            with open(vhost_file, 'w') as f:
                f.write(apache2_config)
        except IOError as e:
            logging.error(f"vhost update failed, couldn't write config: {vhost_file}: {e}")
            return

        self.reload_apache2()

    def vhost_drop(self, schema: Schema):
        vhost_dir = self.cfg.require('autoconf', 'apache2', 'vhost_directory')
        vhost_file = schema.vhost_file_path(vhost_dir)
        os.unlink(vhost_file)

        self.reload_apache2()

    def reload_apache2(self):
        cmd = self.cfg.require('autoconf', 'apache2', 'reload_command')
        r = os.system(cmd)
        if r != 0:
            logging.error(f"command returned {r}: {cmd}")

    def render_apache2_vhost_config(self, schema: Schema) -> str:
        try:
            wanted_version = schema.project_php_version or self.cfg.require('php', 'default_version')
            php_socket = self.cfg.require('php', 'versions', wanted_version, 'socket')
        except KeyError:
            raise SchemaError(f"PHP version unavailable: {wanted_version}")

        vhost_template = self.cfg.require('autoconf', 'apache2', 'vhost_template')
        with open(vhost_template) as f:
            template = jinja2.Template(f.read())

        return template.render(
            name=schema.name,
            document_root=os.path.join(schema.project_dir, schema.project_webroot),
            php_socket=php_socket,
        )
