import logging
import os
import shutil
import sys

from .. import util
from ..config import Config
from ..schema import Schema


def main():
    logging.basicConfig(level=logging.DEBUG)

    util.create_and_become_devbox_user()

    shim_name = sys.argv[1]

    program = resolve_shim_to_program(shim_name)
    args = sys.argv[2:]

    logging.debug(f"os.execl({program}, {shim_name}, *{args})")
    os.execl(program, shim_name, *args)


def resolve_shim_to_program(shim_name: str):
    resolvers = {
        'php': resolve_php,
    }

    resolver = resolvers.get(shim_name)

    if resolver:
        result = resolver()
    else:
        logging.debug("no resolver set for this program")

    if not resolver or not result:
        logging.debug("using shutil")
        result = shutil.which(shim_name)

    return result


def resolve_php():
    if not os.path.exists('/.devbox.yml'):
        return None

    config = Config.load()
    schema = Schema('/.devbox.yml')

    version_key = schema.project_php_version
    if not version_key:
        logging.warning("falling back to default because project has no php version")
        version_key = config.require('php', 'default_version')

    binary = config.require('php', 'versions', version_key, 'binary')
    return binary


if __name__ == '__main__':
    main()
