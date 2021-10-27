#!/bin/sh
set -eu

if [ ! -d /var/lib/mysql/mysql ]; then
  mysql_install_db > /dev/null
fi

exec mysqld --init-file=/init.sql