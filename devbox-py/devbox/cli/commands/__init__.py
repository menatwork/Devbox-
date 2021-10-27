from devbox.cli import Context, Error


COMMANDS = []


class UsageError(Error):
    """
    This error type means that the CLI was called in some invalid way by the
    user, and that a help message should be shown.
    """
    pass


def dispatch(ctx: Context):
    try:
        cmd_name = ctx.args.pop(0)
    except IndexError:
        raise UsageError("Kein Befehl angegeben!")

    cmd_module = find_command(cmd_name)
    cmd_module.call(ctx)


def find_command(s: str) -> any:
    for m in COMMANDS:
        if m.name == s:
            return m

    raise UsageError("Unbekannter Befehl!")


from . import browser, build, exec, pull, push, run, shell_init, shim


COMMANDS = [
    browser,
    build,
    exec,
    pull,
    push,
    run,
    shell_init,
    shim,
]


HELP = {
    "Benutzung": [
        browser,
        exec,
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
