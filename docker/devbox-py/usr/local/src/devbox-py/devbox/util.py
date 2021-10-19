"""
General assorted utilities that don't fit into any particular module.
"""

import os
import subprocess


def create_and_become_devbox_user():
    """
    Create a user named 'devbox' from the environment variables 'DEVBOX_UID' and
    'DEVBOX_GID', and assume its privileges.
    """
    uid = os.environ['DEVBOX_UID']
    gid = os.environ['DEVBOX_GID']

    subprocess.run(['/usr/sbin/groupadd', '--gid', gid, 'devbox'],
                   check=True)

    subprocess.run(['/usr/sbin/useradd', '--uid', uid, '--gid', gid, 'devbox'],
                   check=True)

    os.setgroups([])
    os.setgid(int(gid))
    os.setuid(int(uid))
