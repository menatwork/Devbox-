from devbox.cli import Context


name = 'shell-init'
short_help = "Shell-Code für PATH-Setup erzeugen"
long_help = "TODO"


def call(ctx: Context):
    print(f'PATH="{ctx.repo_dir}/bin:{ctx.repo_dir}/bin/shims:$PATH"')
