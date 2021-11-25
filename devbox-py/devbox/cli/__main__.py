from typing import NoReturn
import logging
import os
import sys

from . import commands, Error, Context
from ..config import Config
import devbox.logging


def main() -> None:
    devbox.logging.init()

    args = sys.argv[1:]  # skip program name
    repo_dir = os.path.normpath(os.environ['DEVBOX_CLI_REPO_DIR'])
    config_dir = os.path.join(repo_dir, 'config')

    config = Config.load_dir(config_dir)

    ctx = Context(
        args=args,
        config=config,
        repo_dir=repo_dir,
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
