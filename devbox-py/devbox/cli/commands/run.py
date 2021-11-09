import logging
import os
import pprint
import sys

from devbox.cli import Context, Error
from devbox.cli.shim import resolve_shim
from devbox.cli.util import find_binary
from devbox.schema import InvalidSchema


name = 'run'
short_help = "Befehle im Devbox-Container ausführen"
long_help = "TODO"


def call(ctx: Context):
    if len(ctx.args) == 0:
        docker_args = server_args(ctx)
    else:
        docker_args = other_command_args(ctx)

    os.execv(find_binary('docker'), docker_args)


def server_args(ctx: Context):
    args = common_args(ctx)
    args.extend([
        '--name', 'devbox-server',
        '--publish', '80:80',
        '--publish', '3306:3306',
        ctx.devbox_image,
        '/server.sh',
    ])
    return args


def other_command_args(ctx: Context):
    try:
        args = common_args(ctx)
        args.append(ctx.devbox_image)
        args.extend(resolve_shim(ctx))
        return args
    except InvalidSchema as e:
        formatted_errors = pprint.pformat(e.errors)
        raise Error(f"Fehlerhafte Schemadatei:\n\n\t{e.file_path}\n\n{formatted_errors}")


def common_args(ctx: Context) -> 'list[str]':
    args = [
        'docker',
        'run',
        '--rm',
        '--interactive',

        '--volume', f'{ctx.repo_dir}/config.yml:/etc/devbox/config.yml:ro',
        '--volume', f'{ctx.repo_dir}/shell:/var/www/shell',

        '--volume', f'devbox-sockets:/run/devbox-sockets',
        '--volume', f'{ctx.config.projects_volume}:/var/www/projects',
        '--volume', f'{ctx.repo_dir}/volumes/devbox-home:/home/devbox',
        '--volume', f'{ctx.repo_dir}/volumes/mariadb:/var/lib/mysql',
        '--volume', f'{ctx.repo_dir}/volumes/php-sessions:/var/lib/php/sessions',

        '--env', f'DEVBOX_UID={os.getuid()}',
        '--env', f'DEVBOX_GID={os.getgid()}',
    ]

    if ctx.config.debug:
        logging.debug('Debug mode is on, mapping devbox-py')
        args.extend(['--volume', f'{ctx.repo_dir}/devbox-py/devbox:/src/devbox-py/devbox'])

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
            '--env', f'SSH_AUTH_SOCK={ssh_auth_sock}',
        ])
    
    return args