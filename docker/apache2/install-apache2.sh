build-helper install apache2

a2enmod --quiet proxy_fcgi proxy_http proxy_wstunnel setenvif rewrite headers
a2enconf --quiet devbox
a2dissite --quiet 000-default

cat >> /etc/apache2/envvars <<EOF

# devbox modifications
export APACHE_RUN_USER=devbox
export APACHE_RUN_GROUP=devbox
EOF
