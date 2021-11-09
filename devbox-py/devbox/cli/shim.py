from dataclasses import dataclass
import logging
import os

from devbox.cli import Context
from devbox.config import Config as DevboxConfig
from devbox.schema import Schema, SchemaNotFound


class ResolverContext(Context):
    shim_name: str
    shim_args: 'list[str]'

    def __init__(self, ctx: Context):
        super().__init__(
            ctx.args, ctx.config, ctx.repo_dir, ctx.devbox_image
        )


def resolve_shim(ctx: Context) -> 'list[str]':
    resolvers = {
        'composer': resolve_composer,
        'composer1': resolve_composer,
        'php': resolve_php,
        'php5.6': resolve_php,
        'php7.3': resolve_php,
        'php7.4': resolve_php,
        'php8.0': resolve_php,
    }

    shim_name = os.path.basename(ctx.args[0])
    resolver = resolvers.get(shim_name)
    if not resolver:
        return [shim_name, *ctx.args[1:]]

    rc = ResolverContext(ctx)
    rc.shim_name = shim_name
    rc.shim_args = ctx.args[1:]
    return resolver(rc)


def resolve_php(rc: ResolverContext) -> 'list[str]':
    return [select_php_binary(rc), *rc.shim_args]


def resolve_composer(rc: ResolverContext) -> 'list[str]':
    return [select_php_binary(rc), f'/usr/local/bin/{rc.shim_name}', *rc.shim_args]


def select_php_binary(rc: ResolverContext) -> str:
    config_file = os.path.join(rc.repo_dir, 'config.yml')
    config = DevboxConfig.load(config_file)

    try:
        schema = Schema.find_and_load('/')
        version_key = schema.project.php
        if not version_key:
            version_key = config.require('php', 'default_version')
            default_php_warning(version_key, "Schema definiert keine PHP-Version")

    except SchemaNotFound:
        version_key = config.require('php', 'default_version')
        default_php_warning(version_key, "keine Schemadatei gefunden")

    return config.require('php', 'versions', version_key, 'binary')


def default_php_warning(version: str, cause: str):
    logging.warning(f"Default-PHP-Version ({version}) wird verwendet: {cause}")