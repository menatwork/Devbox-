import os

from . import UsageError
from devbox.cli import Context, Error
from devbox.cli.util import cmd


name = 'browser'
short_help = "Aktuelles Projekt im Browser öffnen"
long_help = "TODO"


def call(ctx: Context) -> None:
    if len(ctx.args) > 0:
        raise UsageError("Zu viele Parameter")

    cwd = os.getcwd()
    projects_dir = os.path.normpath(ctx.config.projects_dir)
    relative_dir = os.path.relpath(cwd, projects_dir)

    if relative_dir == '.' or relative_dir.startswith('../'):
        raise Error(f"{cwd} ist kein Projektverzeichnis")

    relative_project_dir = relative_dir.split(os.sep)[0]
    cmd('xdg-open', f'http://{relative_project_dir}.devbox.localhost')
