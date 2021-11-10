from types import ModuleType
from typing import List

from .. import Context, Error


COMMANDS: List[ModuleType] = []


class UsageError(Error):
    """
    This error type means that the CLI was called in some invalid way by the
    user, and that a help message should be shown.
    """
    pass


def dispatch(ctx: Context) -> None:
    try:
        cmd_name = ctx.args.pop(0)
    except IndexError:
        raise UsageError("Kein Befehl angegeben!")

    cmd_module = find_command(cmd_name)
    cmd_module.call(ctx)  # type: ignore[attr-defined]


def find_command(s: str) -> ModuleType:
    for m in COMMANDS:
        if m.name == s:  # type: ignore[attr-defined]
            return m

    raise UsageError("Unbekannter Befehl!")


from . import browser, build, pull, push, run, shell_init  # noqa: E402


COMMANDS = [
    browser,
    build,
    pull,
    push,
    run,
    shell_init,
]


HELP = {
    "Benutzung": [
        browser,
        run,
    ],

    "Setup & Updates": [
        build,
        pull,
        shell_init,
    ],

    "Wartung": [
        build,
        push,
    ],
}
