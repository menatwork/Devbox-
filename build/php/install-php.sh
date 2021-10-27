#!/usr/bin/env bash
set -euo pipefail

version="$1"
prefix="php$version"

packages=(
  "$prefix-curl"
  "$prefix-fpm"
  "$prefix-gd"
  "$prefix-imagick"
  "$prefix-intl"
  "$prefix-mbstring"
  "$prefix-mysql"
  "$prefix-soap"
  "$prefix-xml"
  "$prefix-yaml"
  "$prefix-zip"
)

if [[ "$version" == 5.6 ]]; then
  packages+=("$prefix-mcrypt")
fi

devbox-build install "${packages[@]}"

# default binary should never be called, that's what the php shim is for
rm -f /usr/bin/php

# install config
cp /php-fpm.conf.template "/etc/php/$version/fpm/php-fpm.conf"
sed -i "s/{PREFIX}/$prefix/g" "/etc/php/$version/fpm/php-fpm.conf"

# install runit service dir
mkdir -p "/etc/service/$prefix-fpm"
cat > "/etc/service/$prefix-fpm/run" <<EOF
#!/bin/sh
exec php-fpm$version --nodaemonize --fpm-config /etc/php/$version/fpm/php-fpm.conf
EOF
chmod +x "/etc/service/$prefix-fpm/run"