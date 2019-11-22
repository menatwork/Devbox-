FROM ubuntu:bionic

ARG DOCKERDEV_UID
RUN if [ -n "$DOCKERDEV_UID" ]; then usermod -u $DOCKERDEV_UID www-data; fi

COPY files.apt-pre/ /

RUN /opt/devbox/install

COPY files.apt-post/ /
COPY mod_vhost_devbox/mod_vhost_devbox.so /usr/local/lib/apache2/modules/

RUN true \
	&& a2enmod  --quiet proxy_fcgi setenvif rewrite headers vhost_devbox \
	&& a2enconf --quiet php7.3-fpm devbox

CMD ["/usr/bin/supervisord", "-c", "/opt/devbox/supervisord.conf"]
