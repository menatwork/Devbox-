FROM ubuntu:focal

ARG DEVBOX_UID
ARG DEVBOX_GID

RUN usermod -u "$DEVBOX_UID" www-data
RUN groupmod -g "$DEVBOX_GID" www-data

COPY base /

RUN build-helper update \
  && build-helper upgrade \
  && build-helper install runit git openssh-client

COPY apache2 /
RUN build-helper run /install-apache2.sh

COPY mariadb /
RUN build-helper run /install-mariadb.sh

COPY php /
RUN build-helper run /install-php.sh

COPY mailcatcher /
RUN build-helper run /install-mailcatcher.sh

COPY nodejs /
RUN build-helper run /install-nodejs.sh

COPY devbox-py /
RUN build-helper run /install-devbox-py.sh

RUN build-helper shrink

ENTRYPOINT [ "/init" ]
