image_name    := devbox
image_version := latest
image_tag     := $(image_name):$(image_version)

mysql_volume  := $(image_name)-mysql

host_projects_dir := $(HOME)/code

.PHONY: run bash
run: .build
	docker run					\
		-v $(host_projects_dir):/projects	\
		-v $(mysql_volume):/var/lib/mysql	\
		-p 80:80				\
		-p 3306:3306				\
		-p 8081:8081				\
		--name $(image_name)			\
		--rm=true				\
		$(image_tag)

bash:
	docker exec --interactive --tty $(image_name) /bin/bash

.build: Dockerfile mod_vhost_devbox/mod_vhost_devbox.so
	docker build \
		--build-arg DOCKERDEV_UID=$(shell id -u) \
		-t $(image_tag) \
		.
	touch .build

mod_vhost_devbox/mod_vhost_devbox.so:
	$(MAKE) -C ./mod_vhost_devbox
