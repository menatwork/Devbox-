#!/usr/bin/env python3
from configparser import ConfigParser
import logging
import os
import sys

from inotify.constants import *
import cerberus
import inotify.adapters
import yaml


class SchemaError(Exception):
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
                'php-version': { 'type': 'string' },
            }
        }
    }

    def __init__(self, path: str):
        with open(path) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        v = cerberus.Validator(allow_unknown=True)
        v.validate(data, self.SPEC)
        if v.errors:
            raise SchemaError(v.errors)

        self.data = data

        self.path = path
        self.project_dir = os.path.dirname(path)
        self.name = os.path.basename(self.project_dir)

    def to_apache2_vhost_config(self, php_sockets: dict, default_php_version: str) -> str:
        php_version = self.data['project'].get('php-version', default_php_version)
        php_socket = php_sockets[php_version]

        if not php_socket:
            raise SchemaError(f"PHP version unavailable: {php_version}")

        document_root = f"{self.project_dir}/{self.data['project']['webroot']}"

        return f"""
        <VirtualHost *:80>
            ServerName "{self.name}.devbox.localhost"
            DocumentRoot "{document_root}"

            <FilesMatch "\.ph(p|ar)$">
                SetHandler "proxy:unix:{php_socket}|fcgi://localhost"
            </FilesMatch>
        </VirtualHost>
        """


class SchemaFileWatcher(object):
    """
    This is a wrapper around inotify that emits more useful change events for
    project schema files in a project directory.

    A root watch is established on the given `project_root` directory; any
    subdirectories in `project_root` will be monitored for files matching the
    `schema_filename`. If any such files are created, edited, deleted, or moved,
    `SchemaFileWatcher` will emit an event. Each schema file that already exists
    when the watcher is started will also generate an event so initial
    configuration can be done through the same API.

    The emitted event types are:
        - 'update' when schema files are created, edited, or renamed
        - 'remove' when schema files are deleted or renamed

    You'll notice that schema files being renamed emit both an 'update' and a
    'remove' event. This is due to the way the inotify API works. Renaming a
    file causes two events: an IN_MOVED_FROM with the source path that was
    renamed, and an IN_MOVED_TO with the new location of our file. The simplest
    way for us to handle this case is to consider file moves as a pair of
    'remove' and 'update', which is not worth optimizing as long as web server
    reconfiguration is cheap.
    """

    PROJECT_ROOT_MASK = (
        IN_ISDIR | IN_MOVE | IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MOVE_SELF
    )

    PROJECT_DIR_MASK = (
        IN_CREATE | IN_DELETE | IN_CLOSE_WRITE | IN_MOVE
    )

    def __init__(self, project_root: str, schema_filename: str):
        self.project_root = project_root
        self.schema_filename = schema_filename
        self.buffered_events = []
        self._init_watches()

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffered_events:
            logging.debug("returning buffered event before wait")
            return self.buffered_events.pop(0)

        logging.debug("waiting...")
        for (_, type_names, path, filename) in self.i.event_gen(yield_nones=False):
            if path == self.project_root:
                self._dispatch_project_root(type_names, path, filename)
            else:
                self._dispatch_project_dir(type_names, path, filename)

            if self.buffered_events:
                logging.debug("returning buffered event after wait")
                return self.buffered_events.pop(0)

    def _init_watches(self):
        self.i = inotify.adapters.Inotify()
        self.i.add_watch(self.project_root, mask=self.PROJECT_ROOT_MASK)

        # add watches to project dirs existing at startup
        with os.scandir(self.project_root) as it:
            for entry in it:
                if entry.name.startswith('.') or not entry.is_dir():
                    continue
                self._watch_project_dir(entry.path)

    def _dispatch_project_root(self, type_names: 'list[str]', path: str, filename: str):
        fullpath = os.path.join(path, filename)

        if 'IN_MOVED_TO' in type_names or 'IN_CREATE' in type_names:
            self._watch_project_dir(fullpath)
        elif 'IN_MOVED_FROM' in type_names or 'IN_DELETE' in type_names:
            self._unwatch_project_dir(fullpath)

    def _dispatch_project_dir(self, type_names: 'list[str]', path: str, filename: str):
        if filename != self.schema_filename:
            return

        fullpath = os.path.join(path, filename)

        if 'IN_CREATE' in type_names or 'IN_CLOSE_WRITE' in type_names or 'IN_MOVED_TO' in type_names:
            self.buffered_events.append(('update', path, fullpath))
        elif 'IN_DELETE' in type_names or 'IN_MOVED_FROM' in type_names:
            self.buffered_events.append(('remove', path, fullpath))

    def _watch_project_dir(self, path: str):
        self.i.add_watch(path, self.PROJECT_DIR_MASK)

        logging.debug(f"{path}: checking for schema file")
        schema_file_path = os.path.join(path, self.schema_filename)

        if os.path.isfile(schema_file_path) or os.path.islink(schema_file_path):
            self.buffered_events.append(('update', path, schema_file_path))

    def _unwatch_project_dir(self, path: str):
        self.i.remove_watch(path)
        self.buffered_events.append(('remove', path, None))


def main():
    if len(sys.argv) != 2:
        print('error: argument must be a single config file', file=sys.stderr)
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    config = ConfigParser()
    with open(sys.argv[1]) as f:
        config.read_file(f)

    watch_and_update_vhosts(config)


def watch_and_update_vhosts(config: ConfigParser):
    """
    The daemon's main loop, which ingests schema file events from
    `SchemaWatcher` and triggers VHost reconfigurations.
    """
    config_general = config['general']
    project_root = config_general['project_root']
    schema_filename = config_general['schema_filename']

    schemas_by_project_dir = {}

    for event in SchemaFileWatcher(project_root, schema_filename):
        (event_type, project_dir, schema_file_path) = event

        if event_type == 'update':
            try:
                schema = Schema(schema_file_path)
                schemas_by_project_dir[project_dir] = schema
                update_vhost(config, schema)
            except Exception as e:
                logging.error(e)

        elif event_type == 'remove':
            schema = schemas_by_project_dir.pop(project_dir)
            drop_vhost(config, schema)

        else:
            logging.warn(f"ignoring unknown event type from SchemaFileWatcher: {event_type}")


def update_vhost(config: ConfigParser, schema: Schema):
    logging.info(f"updating vhost: {schema.name}")

    default_php_version = config['general']['default_php_version']
    vhost_config_root = config['general']['vhost_config_root']
    php_sockets = config['php_sockets']

    apache2_config = schema.to_apache2_vhost_config(php_sockets, default_php_version)
    vhost_config_path = os.path.join(vhost_config_root, f"{schema.name}.conf")

    with open(vhost_config_path, 'w') as f:
        f.write(apache2_config)

    os.system('apachectl -k graceful')


def drop_vhost(config: ConfigParser, schema: Schema):
    logging.info(f"dropping vhost: {schema.name}")

    vhost_config_root = config['general']['vhost_config_root']
    vhost_config_path = os.path.join(vhost_config_root, f"{schema.name}.conf")

    os.unlink(vhost_config_path)
    os.system('apachectl -k graceful')


if __name__ == '__main__':
    main()
