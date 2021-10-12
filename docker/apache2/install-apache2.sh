build-helper install apache2

a2enmod --quiet proxy_fcgi proxy_http proxy_wstunnel setenvif rewrite headers
a2enconf --quiet devbox
a2dissite --quiet 000-default
