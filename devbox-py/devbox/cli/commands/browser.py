import os

from . import UsageError
from .. import Context, Error
from ..util import cmd


name = 'browser'
short_help = "Aktuelles Projekt im Browser öffnen"
long_help = "TODO"


def call(ctx: Context) -> None:
    if len(ctx.args) > 0:
        raise UsageError("Zu viele Parameter")

    cwd = os.getcwd()
    projects_root = ctx.config.general.projects_root
    relative_dir = os.path.relpath(cwd, projects_root)

    if relative_dir == '.' or relative_dir.startswith('../'):
        raise Error(f"{cwd} ist kein Projektverzeichnis")

    relative_project_dir = relative_dir.split(os.sep)[0]
    url = f'http://{relative_project_dir}.{ctx.config.general.hostname}'

    cmd('xdg-open', url)
