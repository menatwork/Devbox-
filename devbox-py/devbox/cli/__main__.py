from typing import NoReturn
import logging
import os
import sys

from . import commands, Error, Context
from .config import load_dotenv_config, ConfigError
import devbox.logging


def main() -> NoReturn:
    devbox.logging.init()

    args = sys.argv[1:]  # skip program name
    repo_dir = os.path.normpath(os.environ['DEVBOX_CLI_REPO_DIR'])

    try:
        config = load_dotenv_config(os.path.join(repo_dir, '.env'))
    except ConfigError:
        fail(".env konnte nicht geladen werden")

    ctx = Context(
        args=args,
        repo_dir=repo_dir,
        config=config,
        devbox_image='gitlab.men-at-work.de:4774/entwicklung/devbox',
    )

    try:
        commands.dispatch(ctx)
    except commands.UsageError as e:
        fail(str(e), True)
    except Error as e:
        fail(str(e))


def fail(message: str, show_usage: bool = False) -> NoReturn:
    logging.critical(message)
    if show_usage:
        logging.warning("Hilfetext fehlt.")
    sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Von Benutzer unterbrochen", file=sys.stderr)
        sys.exit(1)
