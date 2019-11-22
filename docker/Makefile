image_name		:= devbox
image_version		:= latest
image_tag		:= $(image_name):$(image_version)
container_name		:= $(image_name)

volume_mysql		:= $(image_name)-mysql
volume_composer		:= $(image_name)-composer
volume_sessions		:= $(image_name)-sessions

host_projects_dir	:= $(PWD)/../..
host_devbox_shell_dir   := $(PWD)/../shell

.PHONY: run bash
run: .build
	docker run								\
		--volume=$(volume_composer):/var/www/.composer/cache		\
		--volume=$(volume_mysql):/var/lib/mysql				\
		--volume=$(volume_sessions):/var/lib/php/sessions		\
		--volume=$(host_projects_dir):/projects				\
		--volume=$(host_devbox_shell_dir):/shell			\
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
