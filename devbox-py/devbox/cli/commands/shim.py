from dataclasses import dataclass
import logging
import os
import sys

from devbox.cli import Context, Error
from devbox.cli.util import find_binary
from devbox.config import Config as DevboxConfig
from devbox.schema import Schema, SchemaNotFound


name = 'shim'


@dataclass
class ShimCall(object):
    docker_image: str
    docker_cmd: 'list[str]'
    bind_ssh_agent: bool
    bind_sockets: bool


class ResolverContext(Context):
    shim_name: str
    shim_args: 'list[str]'

    def __init__(self, ctx: Context):
        super().__init__(
            ctx.args, ctx.config, ctx.devbox_image, ctx.repo_dir
        )


def call(ctx: Context):
    if len(ctx.args) < 1:
        raise Error("need at least one parameter")

    logging.debug(f"shim called with: {ctx.args}")

    shim_call = resolve_shim(ctx)

    docker_args = [
        '--rm',
        '--interactive',
    ]

    if sys.stdin.isatty():
        docker_args.append('--tty')

    docker_args.extend([
        '--env', f'DEVBOX_UID={os.getuid()}',
        '--env', f'DEVBOX_GID={os.getgid()}',

        '--volume', f'{os.getcwd()}:/mnt',
        '--workdir', '/mnt',

        '--volume', f'{ctx.repo_dir}/volumes/data/devbox-home:/home/devbox',
    ])

    if shim_call.bind_ssh_agent:
        if ssh_auth_sock := os.getenv('SSH_AUTH_SOCK'):
            docker_args.extend([
                '--volume', f'{ssh_auth_sock}:/run/ssh-agent.sock',
                '--env', f'SSH_AUTH_SOCK=/run/ssh-agent.sock',
            ])
        else:
            logging.warning("Kein SSH-Agent verfügbar!")

    if shim_call.bind_sockets:
        docker_args.extend([
            '--volume', 'devbox_sockets:/run/devbox-sockets',
        ])


    logging.debug(find_binary('docker'))
    logging.debug(['docker', 'run', *docker_args, shim_call.docker_image, *shim_call.docker_cmd])

    os.execv(
        find_binary('docker'),
        ['docker', 'run', *docker_args, shim_call.docker_image, *shim_call.docker_cmd]
    )


def resolve_shim(ctx: Context) -> ShimCall:
    resolvers = {
        'composer': resolve_composer,
        'composer1': resolve_composer,
        'php': resolve_php,
        'php5.6': resolve_php,
        'php7.3': resolve_php,
        'php7.4': resolve_php,
        'php8.0': resolve_php,

        'mysql': resolve_mysql,
        'mysqldump': resolve_mysql,

        'node': resolve_nodejs,
        'npm': resolve_nodejs,
        'yarn': resolve_nodejs,
    }

    shim_name = os.path.basename(ctx.args[0])
    resolver = resolvers.get(shim_name)
    if not resolver:
        raise Error(f"no resolver for shim invocation: {ctx.args}")

    rc = ResolverContext(ctx)
    rc.shim_name = shim_name
    rc.shim_args = ctx.args[1:]
    return resolver(rc)


def resolve_php(rc: ResolverContext) -> ShimCall:
    return ShimCall(
        'devbox_php',
        [select_php_binary(rc), *rc.shim_args],
        bind_ssh_agent=True,
        bind_sockets=True,
    )


def resolve_composer(rc: ResolverContext) -> ShimCall:
    return ShimCall(
        'devbox_php',
        [select_php_binary(rc), f'/usr/local/bin/{rc.shim_name}', *rc.shim_args],
        bind_ssh_agent=True,
        bind_sockets=True,
    )


def select_php_binary(rc: ResolverContext) -> str:
    config_file = os.path.join(rc.repo_dir, 'config', 'config.yml')
    config = DevboxConfig.load(config_file)

    try:
        schema = Schema.find_and_load('/')
        version_key = schema.project_php_version
        if not version_key:
            version_key = config.require('php', 'default_version')
            default_php_warning(version_key, "Schema definiert keine PHP-Version")

    except SchemaNotFound:
        version_key = config.require('php', 'default_version')
        default_php_warning(version_key, "keine Schemadatei gefunden")

    return config.require('php', 'versions', version_key, 'binary')


def default_php_warning(version: str, cause: str):
    logging.warning(f"Default-PHP-Version ({version}) wird verwendet: {cause}")


def resolve_mysql(rc: ResolverContext) -> ShimCall:
    return ShimCall(
        'devbox_mariadb',
        [f'/usr/bin/{rc.shim_name}', *rc.shim_args],
        bind_ssh_agent=False,
        bind_sockets=True,
    )


def resolve_nodejs(rc: ResolverContext) -> ShimCall:
    return ShimCall(
        'devbox_nodejs',
        [f'/usr/bin/{rc.shim_name}', *rc.shim_args],
        bind_ssh_agent=True,
        bind_sockets=True,
    )