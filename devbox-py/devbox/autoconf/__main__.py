from sys import argv, stderr, exit
import logging
import os
import threading

from . import Autoconf, dashboard


def main() -> None:
    if len(argv) != 1:
        print("error: this program takes no arguments", file=stderr)
        exit(1)

    logging.basicConfig(level=logging.INFO)

    os.chdir('/etc/devbox/host')

    dashboard_thread = threading.Thread(target=dashboard.run_server)
    dashboard_thread.start()

    a = Autoconf()
    a.watch_and_update_vhosts()


if __name__ == '__main__':
    main()
