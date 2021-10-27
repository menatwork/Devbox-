FROM ubuntu:focal AS devbox_base

COPY base /

RUN devbox-build update \
    && devbox-build upgrade

ENTRYPOINT ["/entrypoint.sh"]

###############################################################################

FROM devbox_base AS devbox_apache2

RUN devbox-build install \
    apache2 \
    libcap2-bin \
    python3-jinja2 \
    python3-pip \
    python3-wheel \
    python3-yaml \
    runit

COPY apache2/apache2 /

# allow apache2 to use port 80
RUN setcap CAP_NET_BIND_SERVICE=+eip /usr/sbin/apache2 \
    && a2enmod --quiet proxy_fcgi proxy_http proxy_wstunnel setenvif rewrite headers \
    && a2enconf --quiet devbox \
    && a2dissite --quiet 000-default \
    && echo APACHE_RUN_USER=devbox >> /etc/apache2/envvars

COPY apache2/devbox-py /devbox-py

RUN pip3 install --editable /devbox-py

RUN devbox-build shrink

COPY apache2/runit /
COPY apache2/pre-cmd.sh /

VOLUME "/run/devbox-apache2-vhosts"
VOLUME "/run/devbox-sockets"
VOLUME "/var/www"

EXPOSE 80

CMD ["runsvdir", "/etc/service"]

###############################################################################

FROM devbox_base AS devbox_mariadb

RUN devbox-build install mariadb-server

COPY mariadb /

VOLUME "/run/devbox-sockets"
VOLUME "/var/lib/mysql"

CMD ["/cmd.sh"]

###############################################################################

FROM devbox_base AS devbox_php

RUN devbox-build install \
    software-properties-common gnupg curl unzip runit

RUN apt-add-repository --yes ppa:ondrej/php > /dev/null \
    && devbox-build upgrade

COPY php/install-php.sh /
COPY php/php-fpm.conf.template /

# see https://launchpad.net/~ondrej/+archive/ubuntu/php
RUN /install-php.sh 5.6
RUN /install-php.sh 7.3
RUN /install-php.sh 7.4
RUN /install-php.sh 8.0

COPY php/install-composer.sh /

# see https://getcomposer.org/download/
# first arg is binary name, second arg is version
RUN /install-composer.sh composer 2.1.9 \
RUN /install-composer.sh composer1 1.10.23

COPY php/pre-cmd.sh /

RUN mkdir -p /run/mysqld && ln --symbolic /run/devbox-sockets/mariadb /run/mysqld/mysqld.sock

VOLUME "/run/devbox-sockets"
VOLUME "/var/www/projects"

CMD ["runsvdir", "/etc/service"]

###############################################################################

FROM devbox_base AS devbox_nodejs

RUN devbox-build install ca-certificates

COPY nodejs/apt-config /

RUN devbox-build update \
  && devbox-build install nodejs \
  && npm install -g yarn