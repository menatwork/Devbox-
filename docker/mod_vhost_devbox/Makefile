.libs/mod_vhost_devbox.so: mod_vhost_devbox.c
	apxs -lyaml -c $<

.PHONY: clean install

clean:
	rm -rf mod_vhost_devbox.so mod_vhost_devbox.la mod_vhost_devbox.lo mod_vhost_devbox.slo .libs

install: .libs/mod_vhost_devbox.so
	install -Dt /usr/local/lib/apache2/modules $<

