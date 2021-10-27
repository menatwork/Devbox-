import subprocess
import sys

from . import UsageError
from devbox.cli import Context, Error
from devbox.cli.docker import DockerCmd


name = 'exec'
short_help = "Befehl im Devbox-Container ausführen"
long_help = "TODO"


def call(ctx: Context):
    if len(ctx.args) == 0:
        raise UsageError("Mindestens ein Parameter nötig")

    c = DockerCmd('exec', ['--interactive'])

    if sys.stdin.isatty():
        c.arg('--tty')

    c.arg('devbox')
    c.args(ctx.args)

    try:
        c.run()
    except subprocess.CalledProcessError:
        raise Error("Befehl konnte nicht ausgeführt werden")
