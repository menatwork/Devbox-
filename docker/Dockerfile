FROM ubuntu:bionic

ARG DEVBOX_UID
ARG DEVBOX_GID

RUN usermod -u "$DEVBOX_UID" www-data
RUN groupmod -g "$DEVBOX_GID" www-data

COPY files.apt-pre/ /
COPY mod_vhost_devbox /tmp/mod_vhost_devbox

RUN /opt/devbox/install

COPY files.apt-post/ /

RUN true \
	&& a2enmod  --quiet proxy_fcgi setenvif rewrite headers vhost_devbox \
	&& a2enconf --quiet php7.3-fpm devbox

CMD ["/usr/bin/supervisord", "-c", "/opt/devbox/supervisord.conf"]
