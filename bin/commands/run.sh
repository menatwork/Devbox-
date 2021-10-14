# NOTE: double slashes at the start of volume names are required for win32
# compatibility

load_dotenv_or_die DEVBOX_PROJECTS_DIR

case "$#" in
  0) image_tag="latest" ;;
  1) image_tag="$1" ;;
  *)
    echo_error "run: Zu viele Parameter"
    exit 1
esac

docker_args=(
  run

  --volume "$devbox_volume_cache"://var/www/.cache
  --volume "$devbox_volume_mysql"://var/lib/mysql
  --volume "$devbox_volume_sessions"://var/lib/php/sessions
  --volume "$devbox_volume_logs"://var/log
  --volume "$devbox_shell_dir"://shell

  --volume "$DEVBOX_PROJECTS_DIR"://projects

  --publish 80:80
  --publish 3306:3306

  --name devbox
  --tty
  --interactive
  --rm

  "$devbox_image:$image_tag"
)

devbox_docker "${docker_args[@]}"
