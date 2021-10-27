import os

from . import UsageError
from devbox.cli import Context
from devbox.cli.util import find_binary


name = 'run'
short_help = "Devbox-Container ausführen"
long_help = "TODO"


def call(ctx: Context):
    if len(ctx.args) > 0:
        raise UsageError("Zu viele Parameter")

    os.chdir(ctx.repo_dir)

    write_host_env_file()

    os.execve(
        find_binary('docker-compose'),
        ['docker-compose', '--project-name', 'devbox', 'up'],
        env={
            'DEVBOX_REPO_DIR': ctx.repo_dir,
        }
    )


def write_host_env_file():
    with open('tmp/host.env', 'w') as f:
        print(f'DEVBOX_UID={os.getuid()}', file=f)
        print(f'DEVBOX_GID={os.getgid()}', file=f)