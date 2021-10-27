shim() {
  load_dotenv_or_die DEVBOX_PROJECTS_DIR

  if [[ -t 1 ]]; then
    echo_debug "shim called with: $@"
  fi

  local docker_args=(
    --user devbox:devbox
    --env SSH_AUTH_SOCK=/run/ssh-agent-host.socket
    --interactive
  )

  # This check is necessary because Docker will complain about input pipes when
  # --tty is given, so we only pass --tty if we're not part of a pipe.
  if [[ -t 0 ]]; then
    docker_args+=(--tty)
  fi

  local workdir="$(devbox_pwd_in_container)"
  if [[ "$workdir" != "" ]]; then
    docker_args+=(--workdir "$workdir")
  else
    echo_warning "Shim wurde nicht in $DEVBOX_PROJECTS_DIR ausgeführt, Pfad kann nicht gemappt werden"
    docker_args+=(--workdir "/")
  fi

  devbox_docker exec "${docker_args[@]}" devbox devbox-shim "$@"
}

shim "$@"
