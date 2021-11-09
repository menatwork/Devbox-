ARG DEVBOX_BASE_IMAGE
FROM ${DEVBOX_BASE_IMAGE}

COPY docker/base/pre-install /
RUN build-helper run /install-base.sh

COPY docker/apache2/pre-install /
RUN build-helper run /install-apache2.sh

COPY docker/mariadb/pre-install /
RUN build-helper run /install-mariadb.sh

COPY docker/php/pre-install /
RUN build-helper run /install-php.sh

COPY docker/mailcatcher/pre-install /
RUN build-helper run /install-mailcatcher.sh

COPY docker/nodejs/pre-install /
RUN build-helper run /install-nodejs.sh

COPY docker/devbox-py/pre-install /
COPY devbox-py /src/devbox-py
RUN build-helper run /install-devbox-py.sh

RUN build-helper shrink

COPY docker/base/post-install /
COPY docker/apache2/post-install /
COPY docker/mariadb/post-install /
COPY docker/php/post-install /
COPY docker/mailcatcher/post-install /
# nodejs has no post-install dir
COPY docker/devbox-py/post-install /

ARG DEVBOX_VERSION
RUN echo $DEVBOX_VERSION > /etc/devbox/version

ENTRYPOINT [ "/entrypoint.sh" ]
