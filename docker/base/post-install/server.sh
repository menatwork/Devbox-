#!/usr/bin/env bash
set -euo pipefail

cat <<EOF

  MEN AT WORK Devbox $(cat /etc/devbox/version)

  Dashboard:    http://devbox.localhost
  Mailcatcher:  http://mailcatcher.devbox.localhost

  MariaDB:      localhost:3306, user/password: devbox

EOF

trap "on_exit" EXIT

on_exit() {
  kill -HUP $pid
}

runuser -u devbox -- runsvdir /etc/service &
pid=$!
wait
