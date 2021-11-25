from typing import Dict
import logging
import os

import jinja2

import devbox.config
from ..schema import Schema, SchemaError
from ..config import Config
from .watcher import SchemaFileWatcher
from . import dashboard


class Autoconf(object):
    config: Config

    """
    Main application object
    """
    def __init__(self, config: Config) -> None:
        self.cfg = config

    def watch_and_update_vhosts(self) -> None:
        dir = self.cfg.general.projects_root_internal
        schema_file_name = self.cfg.general.schema_file_name

        schemas_by_project_dir: Dict[str, Schema] = {}
        dashboard.schemas_by_project_dir = schemas_by_project_dir

        for event in SchemaFileWatcher(dir, schema_file_name):
            if event.is_new_or_changed():
                try:
                    schema_file_path = event.schema_file_path()

                    schema = Schema.load_file(schema_file_path)
                    schemas_by_project_dir[event.project_dir] = schema

                    logging.debug(f"{schema.project_name}: updating vhost config")
                    self.vhost_update(schema)
                except SchemaError as e:
                    logging.error(f"{schema_file_path}: {e}")
                except Exception as e:
                    logging.error("Unexpected exception:")
                    logging.exception(e)

            elif event.is_gone():
                try:
                    schema = schemas_by_project_dir.pop(event.project_dir)
                    logging.debug(f"{schema.project_name}: dropping vhost config")
                    self.vhost_drop(schema)
                except KeyError:
                    # unrelated directory or file deletion
                    pass

            else:
                logging.warn(f"ignoring unknown watcher event: {event}")

    def vhost_update(self, schema: Schema) -> None:
        try:
            apache2_config = self.render_apache2_vhost_config(schema)
        except IOError as e:
            logging.error(f"vhost update failed, couldn't read template: {e}")
            return
        except jinja2.TemplateError as e:
            logging.error(f"vhost update failed, invalid template: {e}")
            return

        try:
            vhost_file = self.get_apache2_vhost_path(schema)
            with open(vhost_file, 'w') as f:
                f.write(apache2_config)
        except IOError as e:
            logging.error(f"vhost update failed, couldn't write config: {vhost_file}: {e}")
            return

        self.reload_apache2()

    def vhost_drop(self, schema: Schema) -> None:
        vhost_file = self.get_apache2_vhost_path(schema)
        os.unlink(vhost_file)
        self.reload_apache2()

    def reload_apache2(self) -> None:
        cmd = self.cfg.autoconf.reload_command
        r = os.system(cmd)
        if r != 0:
            logging.error(f"command returned {r}: {cmd}")

    def render_apache2_vhost_config(self, schema: Schema) -> str:
        wanted_version = schema.project.php or self.cfg.php.default_version

        try:
            php_socket = self.cfg.php.versions[wanted_version].socket
        except KeyError:
            raise SchemaError(f"PHP version unavailable: {wanted_version}")

        with open('templates/apache-vhost.conf.j2') as f:
            template = jinja2.Template(f.read())
        
        if not schema.project_directory:
            raise RuntimeError("schema.project_directory is None; this shouldn't happen")
        
        if not schema.project.webroot:
            raise SchemaError("project has no webroot")

        return template.render(
            name=schema.project_name,
            document_root=os.path.join(schema.project_directory, schema.project.webroot),
            php_socket=php_socket,
        )

    def get_apache2_vhost_path(self, schema: Schema) -> str:
        return os.path.join(
            self.cfg.autoconf.vhost_directory,
            f'{schema.project_name}.conf'
        )