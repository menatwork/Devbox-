import os
import shutil
import subprocess

from devbox.cli import Error


def cmd(*args: str, env: 'dict[str, str]' = None) -> None:
    """
    Convenience function for subprocess.run(..., check=True)
    """
    pid = None
    try:
        p = subprocess.Popen(args, env=env)
        pid = p.pid
        returncode = p.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, args)
    except KeyboardInterrupt as e:
        if pid:
            os.waitpid(pid, 0)
        raise e


def cmd_get_stdout(*args: str) -> str:
    """
    Convenience function for subprocess.run(..., check=True,
    stdout=subprocess.PIPE) and subsequent output decoding
    """
    p = subprocess.run(args, check=True, stdout=subprocess.PIPE)
    s = p.stdout.decode().strip()
    return s


def find_binary(s: str) -> str:
    if b := shutil.which(s):
        return b
    else:
        raise Error(f"{s} not found in PATH")
