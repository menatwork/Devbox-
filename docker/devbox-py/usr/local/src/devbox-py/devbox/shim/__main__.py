from typing import Tuple
import logging
import os
import shutil
import sys

from ..config import Config
from ..schema import Schema, SchemaNotFound


class NoResolver(Exception):
    pass


class NoSchema(Exception):
    pass


def main():
    logging.basicConfig(level=logging.ERROR)

    shim_name = os.path.basename(sys.argv[1])
    args = sys.argv[2:]

    try:
        program, args = resolve_shim(shim_name, args)
        logging.debug(f"resolved: program={program}, args={args}")
    except NoResolver:
        logging.debug("no resolver for this program, using shutil")
        program = shutil.which(shim_name)

    shim_name = os.path.basename(program)

    logging.debug(f"os.execl({program}, {shim_name}, *{args})")
    os.execl(program, shim_name, *args)


def resolve_shim(shim_name: str, args: 'list[str]') -> Tuple[str, 'list[str]']:
    resolvers = {
        'php': resolve_php,
        'composer': resolve_composer,
        'composer1': resolve_composer,
    }

    resolver = resolvers.get(shim_name)
    if not resolver:
        raise NoResolver()

    return resolver(shim_name, args)


def resolve_php(_name, args):
    return (select_php_binary(), args)


def resolve_composer(name, args):
    return (
        select_php_binary(),
        [f'/usr/local/bin/{name}', *args]
    )


def select_php_binary():
    config = Config.load()
    projects_root = config.require('general', 'projects_root')

    try:
        schema = Schema.find_and_load(projects_root)
        version_key = schema.project_php_version
        if not version_key:
            logging.warning("falling back to default because project has no php version")
            version_key = config.require('php', 'default_version')

    except SchemaNotFound:
        logging.warning("falling back to default because no schema was found")
        version_key = config.require('php', 'default_version')

    return config.require('php', 'versions', version_key, 'binary')


if __name__ == '__main__':
    main()
