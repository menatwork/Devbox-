image_name		:= devbox
image_version		:= latest
image_tag		:= $(image_name):$(image_version)
container_name		:= $(image_name)

mysql_volume		:= $(image_name)-mysql

host_cache_dir		:= $(HOME)/.cache/devbox
host_projects_dir	:= $(HOME)/code
host_devbox_shell_dir   := $(PWD)/../shell

.PHONY: run bash
run: .build
	docker run								\
		--volume=$(host_cache_dir)/composer:/var/www/.composer/cache	\
		--volume=$(host_projects_dir):/projects				\
		--volume=$(host_devbox_shell_dir):/shell			\
		--volume=$(mysql_volume):/var/lib/mysql				\
		--publish 80:80							\
		--publish 1080:1080						\
		--publish 3306:3306						\
		--publish 8081:8081						\
		--name=$(container_name)					\
		--rm=true							\
		$(container_name)

bash:
	docker exec --interactive --tty $(container_name) /bin/bash

.build: Dockerfile mod_vhost_devbox/mod_vhost_devbox.so
	docker build						\
		--build-arg DOCKERDEV_UID=$(shell id -u)	\
		--tag=$(image_tag)				\
		.
	touch .build

mod_vhost_devbox/mod_vhost_devbox.so:
	$(MAKE) -C ./mod_vhost_devbox
