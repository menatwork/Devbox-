ARG DEVBOX_BASE_IMAGE
FROM ${DEVBOX_BASE_IMAGE}

COPY base /

RUN build-helper update \
  && build-helper upgrade \
  && build-helper install runit git openssh-client htop rsync

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

ARG DEVBOX_VERSION
RUN echo $DEVBOX_VERSION > /etc/devbox/version

ENTRYPOINT [ "/init" ]
