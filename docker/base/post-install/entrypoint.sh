#!/bin/sh
set -eu

# Create ephemeral devbox user with host UID/GID so host volumes can be accessed
groupadd --gid "$DEVBOX_GID" devbox
useradd --uid "$DEVBOX_UID" --gid "$DEVBOX_GID" devbox

# Create runtime dirs that don't exist yet
install -m 755 -d \
  /run/apache2/devbox-vhosts \
  /run/mysqld \
  /run/php \
  /var/log/apache2 \
  /var/log/mysql

# Ensure devbox user can access everything it needs
chown --recursive devbox:devbox \
  /etc/service \
  /run \
  /var/lock \
  /var/log \
  /home/devbox \
  /var/lib/mysql \
  /var/lib/php/sessions

# Allow dnsmasq to listen on port 53 because resolv.conf doesn't let us specify
# a different port for the system resolver
setcap cap_net_bind_service=+ep /usr/sbin/dnsmasq

# Replace resolv.conf copied from host with our own version
cp /etc/resolv_custom.conf /etc/resolv.conf

exec "$@"
