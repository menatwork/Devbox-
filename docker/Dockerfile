FROM ubuntu:bionic

ARG DOCKERDEV_UID
RUN if [ -n "$DOCKERDEV_UID" ]; then usermod -u $DOCKERDEV_UID www-data; fi

COPY files.apt-pre/ /

RUN export DEBIAN_FRONTEND=noninteractive \
	&& apt-get update -qq \
	&& apt-get install -qq software-properties-common \
	&& apt-add-repository --yes ppa:ondrej/php \
	&& apt-get install -qq \
	libyaml-0-2 supervisor apache2 mariadb-server composer \
	\
	php7.3-fpm php7.3-xml php7.3-curl php7.3-intl php7.3-gd php7.3-imagick \
	php7.3-mbstring php7.3-zip php7.3-mysql php7.3-soap \
	\
	php5.6-fpm php5.6-xml php5.6-curl php5.6-intl php5.6-gd php5.6-imagick \
	php5.6-mbstring php5.6-zip php5.6-mysql php5.6-soap php5.6-mcrypt

COPY files.apt-post/ /
COPY mod_vhost_devbox/mod_vhost_devbox.so /usr/local/lib/apache2/modules/

RUN true \
	&& a2enmod   --quiet proxy_fcgi setenvif rewrite headers vhost_devbox \
	&& a2enconf  --quiet php7.3-fpm devbox \
	&& a2dissite --quiet 000-default \
	&& a2ensite  --quiet devbox

CMD ["/usr/bin/supervisord", "-c", "/opt/devbox/supervisord.conf"]
