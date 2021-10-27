from sys import argv, stderr, exit
import logging
import os

from .autoconf import Autoconf


def main():
    if len(argv) != 1:
        print("error: this program takes no arguments", file=stderr)
        exit(1)

    logging.basicConfig(level=logging.INFO)

    os.chdir('/etc/devbox')

    a = Autoconf()
    a.watch_and_update_vhosts()


if __name__ == '__main__':
    main()
