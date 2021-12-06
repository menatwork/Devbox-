import logging
import os
import pprint
import shutil
import subprocess
import sys

from . import UsageError
from .. import Context, Error
from ...schema import Schema
from ..util import cmd


name = 'resources'
short_help = "Seitendaten im aktuellen Projekt verwalten"
long_help = "TODO"


def call(ctx: Context) -> None:
    try:
        subcommand = ctx.args[0]
    except IndexError:
        raise UsageError("Zu wenig Parameter")

    subcommands = {
        'sync': sync,
        'clean': clean,
    }

    try:
        f = subcommands[subcommand]

        schema = Schema.find_and_load(
            ctx.config.general.projects_root,
            ctx.config.general.schema_file_name,
        )

        os.chdir(schema.project_directory)
        f(ctx, schema)
    except KeyError:
        raise UsageError(f"Unbekannter Befehl: resources {subcommand}")


def sync(ctx: Context, schema: Schema) -> None:
    try:
        instance_name = ctx.args[1]
    except IndexError:
        raise UsageError("Instanz-Name fehlt")

    try:
        instance = schema.instances[instance_name]
    except KeyError:
        raise Error(f"Unbekannter Instanz-Name: {instance_name}")
    
    logging.info(f"Synchronisiere Seitendaten von '{instance_name}'...")
    
    remote = f'{instance.ssh.user}@{instance.ssh.host}'
    some_failed = False

    for path in schema.project.resources:
        logging.info(f"-> {path}")

        if instance.deployment.method == 'deployer':
            remote_path = os.path.join(instance.deployment.dir, 'shared', path)
        else:
            remote_path = os.path.join(instance.deployment.dir, path)

        src = f'{remote}:{remote_path}'

        rsync_cmd = [
            'rsync',

            '--archive',
            '--delete',
            '--no-implied-dirs',

            '--compress',
            '--partial',
            '--progress',

            src,
            path
        ]

        logging.debug(f"Running rsync:\n{pprint.pformat(rsync_cmd)}")

        try:
            cmd(*rsync_cmd)
        except subprocess.CalledProcessError as e:
            logging.error(f"Sync von {path} Fehlgeschlagen")
            some_failed = True
    
    if some_failed:
        logging.error("Nicht alle Pfade konnten synchronisiert werden")
        sys.exit(1)
    else:
        logging.info(f"Seitendaten von '{instance_name}' erfolgreich synchronisiert")


def clean(ctx: Context, schema: Schema) -> None:
    logging.warning("Wirklich alle lokalen Seitendaten entfernen?")
    logging.warning("(Enter um fortzufahren, Ctrl-C um abzubrechen)")
    input()

    for path in schema.project.resources:
        logging.info(f"Lösche {path}...")

        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.unlink(path)
    
    logging.info("Seitendaten gelöscht")