#!/bin/sh
set -eu
install -o devbox -g devbox -d /run/apache2 /run/devbox-apache2-vhosts
chown -R devbox:devbox /run/apache2 /etc/service /var/log/apache2