# see https://launchpad.net/~ondrej/+archive/ubuntu/php
php_versions=(
  5.6
  7.3
  7.4
  8.0
  8.1
  8.2
)

# see https://getcomposer.org/download/
composer_1_version=1.10.26
composer_2_version=2.5.1

install_php_versions() {
  local p=()

  for version; do
    local prefix="php$version"

    p+=(
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
      "$prefix-gmp"
      "$prefix-bcmath"
    )

    if [[ "$version" == 5.6 ]]; then
      p+=("$prefix-mcrypt")
    fi
  done

  build-helper install "${p[@]}"
}

build-helper install software-properties-common gnupg curl unzip
apt-add-repository --yes ppa:ondrej/php > /dev/null

install_php_versions "${php_versions[@]}"

# the default binary should never be called, that's what the php shim inside the
# container is for
rm /usr/bin/php

curl --silent --location \
  "https://getcomposer.org/download/$composer_1_version/composer.phar" --output /usr/local/bin/composer1 \
  "https://getcomposer.org/download/$composer_2_version/composer.phar" --output /usr/local/bin/composer

chmod +x /usr/local/bin/composer1 /usr/local/bin/composer
