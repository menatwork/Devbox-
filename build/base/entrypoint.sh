#!/usr/bin/env bash
set -eu

if [[ -v DEVBOX_DEBUG && "$DEVBOX_DEBUG" == 1 ]]; then
    set -x
fi

# Create ephemeral devbox user with host UID/GID so host volumes can be accessed
grep -q ^devbox: /etc/group || groupadd --gid "$DEVBOX_GID" devbox
grep -q ^devbox: /etc/passwd || useradd --uid "$DEVBOX_UID" --gid "$DEVBOX_GID" devbox

if [ -e /pre-cmd.sh ]; then
    /pre-cmd.sh
fi

exec runuser -u devbox -- "$@"