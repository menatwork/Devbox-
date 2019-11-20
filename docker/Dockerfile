FROM ubuntu:bionic

ARG DOCKERDEV_UID
RUN if [ -n "$DOCKERDEV_UID" ]; then usermod -u $DOCKERDEV_UID www-data; fi

COPY conf/99apt-cache /etc/apt/apt.conf.d/99apt-cache

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

COPY mod_vhost_devbox/mod_vhost_devbox.so /usr/local/lib/apache2/modules/
COPY conf/vhost_devbox.load /etc/apache2/mods-available/

COPY conf/apache2-devbox.conf /etc/apache2/conf-available/devbox.conf
COPY conf/apache2-devbox-vhost.conf /etc/apache2/sites-available/devbox.conf

RUN true \
	&& sed -i -E s,/run/php/,/run/, /etc/apache2/conf-available/php*-fpm.conf \
	&& a2enmod   --quiet proxy_fcgi setenvif rewrite headers vhost_devbox \
	&& a2enconf  --quiet php7.3-fpm devbox \
	&& a2dissite --quiet 000-default \
	&& a2ensite  --quiet devbox

COPY conf/php5.6-fpm.conf /etc/php/5.6/fpm/php-fpm.conf
COPY conf/php7.3-fpm.conf /etc/php/7.3/fpm/php-fpm.conf

RUN sed -i -E "s,^(bind-address		)= 127.0.0.1$,\1= 0.0.0.0," \
	/etc/mysql/mariadb.conf.d/50-server.cnf

COPY conf/mariadb_init.sql /
COPY start-mariadb /usr/local/sbin/

COPY start-php-fpm /usr/local/sbin/

COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
