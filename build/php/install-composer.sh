#!/usr/bin/env bash
set -euo pipefail

binary="/usr/local/bin/$1"
version="$2"

curl --silent --location \
  "https://getcomposer.org/download/$version/composer.phar" \
  --output "$binary" \

chmod +x "$binary"
