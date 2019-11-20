mod_vhost_devbox.so: mod_vhost_devbox.c
	apxs -lyaml -c $<
	cp .libs/$@ .

.PHONY: clean
clean:
	rm -rf mod_vhost_devbox.so mod_vhost_devbox.la mod_vhost_devbox.lo mod_vhost_devbox.slo .libs

