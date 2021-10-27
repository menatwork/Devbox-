#!/bin/sh
set -eu

chown --recursive devbox:devbox /etc/runit

if [ -d /home/devbox ]; then
  chown --recursive devbox:devbox /home/devbox
fi

if [ -d /run/devbox-sockets ]; then
  chown --recursive devbox:devbox /run/devbox-sockets
fi

if [ -d /var/log/php ]; then
  chown --recursive devbox:devbox /var/log/php
fi