from typing import List
import logging
import os
import pprint
import sys

from devbox.cli import Context, Error
from devbox.cli.docker import ensure_devbox_network_exists
from devbox.cli.shim import resolve_shim
from devbox.cli.util import find_binary
from devbox.schema import InvalidSchema


name = 'run'
short_help = "Befehle im Devbox-Container ausführen"
long_help = "TODO"


def call(ctx: Context) -> None:
    if len(ctx.args) == 0:
        docker_args = server_args(ctx)
    else:
        docker_args = other_command_args(ctx)

    ensure_devbox_network_exists()

    logging.debug(f"Running command: {pprint.pformat(docker_args)}")
    os.execv(find_binary('docker'), docker_args)


def server_args(ctx: Context) -> List[str]:
    args = common_args(ctx)
    args.extend([
        '--name', 'devbox-server',
        '--publish', '80:80',
        '--publish', '3306:3306',
        ctx.devbox_image,
        '/server.sh',
    ])
    return args


def other_command_args(ctx: Context) -> List[str]:
    host_workdir = os.getcwd()
    if not host_workdir.startswith(ctx.config.projects_dir):
        raise Error("Nicht im Projektverzeichnis")

    args = common_args(ctx)

    workdir = host_workdir.replace(ctx.config.projects_dir, '/var/www/projects')
    args.extend([
        '--workdir', workdir,
        ctx.devbox_image,
        'runuser', '-u', 'devbox', '--'
    ])
    
    try:
        args.extend(resolve_shim(ctx))
    except InvalidSchema as e:
        formatted_errors = pprint.pformat(e.errors)
        raise Error(
            "Fehlerhafte Schemadatei:\n\n"
            f"\t{e.file_path}\n\n"
            f"{formatted_errors}"
        )

    return args


def common_args(ctx: Context) -> List[str]:
    args = [
        'docker',
        'run',
        '--rm',
        '--interactive',

        '--network', 'devbox',

        '--volume',
        f'{ctx.repo_dir}/config/config.yml:/etc/devbox/config.yml:ro',

        '--volume', f'devbox-sockets:/run/devbox-sockets',
        '--volume', f'{ctx.config.projects_volume}:/var/www/projects',
        '--volume', f'{ctx.repo_dir}/shell:/var/www/shell',
        '--volume', f'{ctx.repo_dir}/volumes/devbox-home:/home/devbox',
        '--volume', f'{ctx.repo_dir}/volumes/logs/apache2:/var/log/apache2',
        '--volume', f'{ctx.repo_dir}/volumes/logs/mariadb:/var/log/mysql',
        '--volume', f'{ctx.repo_dir}/volumes/logs/php:/var/log/php',
        '--volume', f'{ctx.repo_dir}/volumes/mariadb:/var/lib/mysql',
        '--volume', f'{ctx.repo_dir}/volumes/php-sessions:/var/lib/php/sessions',  # noqa: E501

        '--env', f'DEVBOX_UID={os.getuid()}',
        '--env', f'DEVBOX_GID={os.getgid()}',
    ]

    if ctx.config.debug:
        logging.debug('Debug mode is on, mapping devbox-py')
        args.extend([
            '--volume',
            f'{ctx.repo_dir}/devbox-py/devbox:/src/devbox-py/devbox'
        ])

    if os.path.exists('/etc/localtime'):
        logging.debug("Mapping host timezone")
        args.extend(['--volume', '/etc/localtime:/etc/localtime:ro'])

    if sys.stdin.isatty():
        logging.debug('TTY detected, passing --tty')
        args.append('--tty')

    if ssh_auth_sock := os.getenv('SSH_AUTH_SOCK'):
        logging.debug("Mapping host SSH agent")
        args.extend([
            '--volume', f'{ssh_auth_sock}:/run/ssh-agent-host.sock',
            '--env', f'SSH_AUTH_SOCK=/run/ssh-agent-host.sock',
        ])

    return args
