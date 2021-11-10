import logging
import os

from . import UsageError
from devbox.cli import Context
from devbox.cli.util import cmd, cmd_get_stdout


name = 'build'
short_help = "Devbox-Image bauen"
long_help = "TODO"


def call(ctx: Context) -> None:
    # just in case we're not in the devbox repo
    os.chdir(ctx.repo_dir)

    base_image = 'ubuntu:focal'
    build_tag = 'latest'

    if len(ctx.args) == 0:
        logging.info(
            f"Keine Version angegeben; Build wird mit ':{build_tag}' getaggt."
        )

    elif len(ctx.args) == 1:
        build_tag = ctx.args[0]

        if not git_tag_exists(build_tag):
            raise UsageError("Release-Tag fehlt!")

        logging.info(f"Release-Build mit Tag '{build_tag}' wird erstellt...")

    else:
        raise UsageError("Zu viele Parameter")

    version = build_tag
    if build_tag == 'latest':
        version = latest_version_string()

    logging.info(f"Basis-Image wird aktualisiert: {base_image}")
    cmd('docker', 'pull', base_image)

    full_tag = f'{ctx.devbox_image}:{build_tag}'
    logging.info("Baue Image...")
    cmd(
        'docker', 'build',
        '--build-arg', f'DEVBOX_BASE_IMAGE={base_image}',
        '--build-arg', f'DEVBOX_VERSION={version}',
        '--tag', full_tag,
        '.'
    )


def git_tag_exists(tag: str) -> bool:
    s = cmd_get_stdout('git', 'tag', '--points-at', 'HEAD')

    for line in s.splitlines():
        if line == tag:
            return True

    return False


def latest_version_string() -> str:
    version = cmd_get_stdout('git', 'rev-parse', '--short', 'HEAD')
    diff = cmd_get_stdout('git', 'diff', '--stat')

    if len(diff) != 0:
        version += '*'

    return version
