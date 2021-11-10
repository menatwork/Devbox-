import subprocess

from . import UsageError
from devbox.cli import Context, Error
from devbox.cli.util import cmd


name = 'pull'
short_help = "Devbox-Image neu beziehen"
long_help = "TODO"


def call(ctx: Context) -> None:
    if len(ctx.args) != 0:
        raise UsageError("Zu viele Parameter")

    try:
        cmd('docker', 'image', 'pull', ctx.devbox_image)
    except subprocess.CalledProcessError:
        raise Error("Befehl konnte nicht ausgeführt werden")
