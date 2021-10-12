build-helper install software-properties-common gnupg curl unzip
apt-add-repository --yes ppa:ondrej/php > /dev/null

composer_1_version=1.10.22
composer_2_version=2.1.8

pkgs=(
  php7.4-fpm php7.4-xml php7.4-curl php7.4-intl php7.4-gd php7.4-imagick
  php7.4-mbstring php7.4-zip php7.4-mysql php7.4-soap php7.4-yaml

  php7.3-fpm php7.3-xml php7.3-curl php7.3-intl php7.3-gd php7.3-imagick
  php7.3-mbstring php7.3-zip php7.3-mysql php7.3-soap php7.3-yaml

  php5.6-fpm php5.6-xml php5.6-curl php5.6-intl php5.6-gd php5.6-imagick
  php5.6-mbstring php5.6-zip php5.6-mysql php5.6-soap php5.6-mcrypt
)

build-helper install "${pkgs[@]}"

curl --silent --location --output /usr/local/bin/composer1 \
    https://getcomposer.org/download/"$composer_1_version"/composer.phar

curl --silent --location --output /usr/local/bin/composer \
    https://getcomposer.org/download/"$composer_2_version"/composer.phar

chmod +x /usr/local/bin/composer1 /usr/local/bin/composer
