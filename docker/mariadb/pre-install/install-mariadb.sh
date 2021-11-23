build-helper install mariadb-server

# mutes warning about user option not being available because we already run
# mariadb as an unprivileged user
sed -iE 's/^user\s\+=\s\+mysql$/#\0/' /etc/mysql/mariadb.conf.d/50-server.cnf
