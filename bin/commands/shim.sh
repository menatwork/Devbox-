shim() {
  load_dotenv_or_die DEVBOX_PROJECTS_DIR

  echo_debug "shim called with: $@"

  local shim_name="$(basename "$1")"
  shift

  shim_args=("$shim_name" "$@")

  run_args=(
    --network host
    --interactive
    --tty
    --rm

    --env DEVBOX_UID="$(id --user)"
    --env DEVBOX_GID="$(id --group)"

    --env DEVBOX_IMAGE="$devbox_image"
    --env DEVBOX_PROJECTS_DIR="$DEVBOX_PROJECTS_DIR"

    --volume "$PWD:/mnt"
    --workdir "/mnt"

    --volume "/var/run/docker.sock:/var/run/docker.sock"
    --volume "/usr/bin/docker:/usr/local/bin/docker:ro"
    --volume devbox-cache:/var/www/.cache
  )

  add_entrypoint
  add_project_schema_file

  devbox_docker run "${run_args[@]}" "$devbox_image" "${shim_args[@]}"
}

# the cli's view of the host fs is currently limited to the directory `devbox`
# is called from. a relevant schema file, if any, must be provided at a known
# location so things like version selection during shim dispatch can work.
add_project_schema_file() {
  local dir="$PWD" f=

  while [[ "$dir" != / ]]; do
    f="$dir/.devbox.yml"

    if [[ -e "$f" ]]; then
      echo_info "Es wird folgende Schemadatei verwendet: $f"
      run_args+=(--volume "$f:/.devbox.yml:ro")
      return
    fi

    dir="$(dirname "$dir")"
  done

  echo_warning "Keine Schemadatei in $PWD oder darüber gefunden"
}

# with DEVBOX_CLI_DEBUG set, the shim handler is executed from the host-side
# source code so we can hack on it without rebuilding the container after every
# change
add_entrypoint() {
  if is_debug; then
    echo_debug "DEVBOX_CLI_DEBUG is 1, shim handler will run from host source"
    run_args+=(
      --volume "$devbox_src_dir/docker/devbox-py/usr/local/src/devbox-py:/src"
      --env PYTHONPATH="/src"
      --entrypoint /usr/bin/python3
    )
    shim_args=(-m devbox.shim "${shim_args[@]}")
  else
    run_args+=(--entrypoint /usr/local/bin/devbox-shim)
  fi
}

shim "$@"
