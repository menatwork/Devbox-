import subprocess

from . import UsageError
from devbox.cli import Context, Error
from devbox.cli.util import cmd


name = 'push'
short_help = "Devbox-Image ins Registry schieben"
long_help = "TODO"


def call(ctx: Context) -> None:
    if len(ctx.args) == 0:
        raise UsageError("Kein Tag-Parameter")
    elif len(ctx.args) == 1:
        push_tag = ctx.args[0]
    else:
        raise UsageError("Zu viele Parameter")

    server_image = ctx.config.docker.server_image

    try:
        cmd('docker', 'image', 'push', f'{server_image}:{push_tag}')
    except subprocess.CalledProcessError:
        raise Error("Befehl konnte nicht ausgeführt werden")
