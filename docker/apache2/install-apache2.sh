build-helper install apache2 libcap2-bin

a2enmod --quiet proxy_fcgi proxy_http proxy_wstunnel setenvif rewrite headers
a2enconf --quiet devbox
a2dissite --quiet 000-default

# allow apache to bind to port 80 without being root
setcap CAP_NET_BIND_SERVICE=+eip /usr/sbin/apache2

echo APACHE_RUN_USER=devbox >> /etc/apache2/envvars
