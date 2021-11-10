from typing import List, Optional
import logging
import os

from devbox.cli import Context
from devbox.config import Config as DevboxConfig
from devbox.schema import Schema, SchemaNotFound


class ResolverContext(Context):
    shim_name: str
    shim_args: List[str]

    def __init__(self, ctx: Context):
        super().__init__(
            ctx.args, ctx.config, ctx.repo_dir, ctx.devbox_image
        )


def resolve_shim(ctx: Context) -> List[str]:
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


def resolve_php(rc: ResolverContext) -> List[str]:
    return [select_php_binary(rc), *rc.shim_args]


def resolve_composer(rc: ResolverContext) -> List[str]:
    return [
        select_php_binary(rc), f'/usr/local/bin/{rc.shim_name}',
        *rc.shim_args
    ]


def select_php_binary(rc: ResolverContext) -> str:

    def get_version_key(config: DevboxConfig, schema: Optional[Schema],
                        warning_text: str) -> str:
        if schema and schema.project.php:
            return schema.project.php
        else:
            default_version = config.require('php', 'default_version')
            logging.warning(
                f"Default-PHP-Version ({default_version}) wird verwendet: "
                f"{warning_text}"
            )
            return default_version

    config_file = os.path.join(rc.repo_dir, 'config.yml')
    config = DevboxConfig.load(config_file)

    try:
        schema = Schema.find_and_load('/')
        version_key = get_version_key(
            config, schema, "Schema definiert keine PHP-Version"
        )
    except SchemaNotFound:
        version_key = get_version_key(
            config, None, "keine Schemadatei gefunden"
        )

    return config.require('php', 'versions', version_key, 'binary')
