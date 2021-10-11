FROM ubuntu:focal

ARG DEVBOX_UID
ARG DEVBOX_GID

RUN usermod -u "$DEVBOX_UID" www-data
RUN groupmod -g "$DEVBOX_GID" www-data

COPY files.apt-pre/ /

RUN /install

COPY files.apt-post/ /

RUN true \
	&& a2enmod  --quiet proxy_fcgi setenvif rewrite headers \
	&& a2enconf --quiet devbox

ENTRYPOINT ["/init"]
