import os

from . import UsageError
from .. import Context, Error
from ...schema import Schema
from ..util import find_binary


name = 'ssh'
short_help = "Per SSH in Instanz einwählen"
long_help = "TODO"


def call(ctx: Context) -> None:
    try:
        target_instance_name = ctx.args[0]
    except IndexError:
        raise UsageError("Zu wenig Parameter")

    schema = Schema.find_and_load(
        ctx.config.general.projects_root,
        ctx.config.general.schema_file_name,
    )

    if not schema.instances:
        raise Error("Schema enthält keine Instanzen")
    
    if target_instance_name not in schema.instances:
        raise Error(f"Schema enthält keine Instanz namens '{target_instance_name}'")
    
    target_ssh = schema.instances[target_instance_name].ssh
    target_string = f'{target_ssh.user}@{target_ssh.host}'

    os.execv(find_binary('ssh'), ['ssh', target_string, *ctx.args[1:]])