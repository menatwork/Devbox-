# NOTE: double slashes at the start of volume mount points are required for
# win32 compatibility

load_dotenv_or_die DEVBOX_PROJECTS_DIR

case "$#" in
  0) image_tag="latest" ;;
  1) image_tag="$1" ;;
  *)
    echo_error "run: Zu viele Parameter"
    exit 1
esac

docker_args=()

if [[ -v SSH_AUTH_SOCK ]]; then
  echo_debug "Mapping host SSH_AUTH_SOCK"
  docker_args+=(--volume "$SSH_AUTH_SOCK"://run/ssh-agent.socket)
fi

if [[ -e /etc/localtime ]]; then
  echo_debug "Mapping host timezone"
  docker_args+=(--volume /etc/localtime://etc/localtime:ro)
fi

docker_args=(
  --volume "$devbox_volume_cache"://home/devbox/.cache
  --volume "$devbox_volume_mysql"://var/lib/mysql
  --volume "$devbox_volume_sessions"://var/lib/php/sessions
  --volume "$devbox_volume_logs"://var/log
  --volume "$devbox_shell_dir"://var/www/shell

  --volume "$DEVBOX_PROJECTS_DIR"://var/www/projects

  --env DEVBOX_UID="$(id --user)"
  --env DEVBOX_GID="$(id --group)"

  --publish 80:80
  --publish 3306:3306

  --name devbox
  --tty
  --interactive
  --rm

  "$devbox_image:$image_tag"
)

devbox_docker run "${docker_args[@]}"
