build() {
  # just in case we're not in the devbox repo
  cd "$devbox_src_dir"

  local base_image=ubuntu:focal
  local version_tag=latest

  if [[ $# != 1 ]]; then
    echo_info "Keine Version angegeben; Build wird mit ':$version_tag' getaggt."
  elif ! git tag --points-at HEAD | grep --quiet "^$1$"; then
    echo_error "Build mit Versionstag '$1' angefordert, aber kein solcher Git-Tag zeigt auf HEAD."
    exit 1
  else
    echo_info "Release-Build mit Versionstag '$1' wird erstellt..."
    image_tag="$1"
  fi

  local version="$version_tag"
  if [[ "$version" == latest ]]; then
    version="$(git rev-parse --short HEAD)"

    if [[ $(git diff --stat) != "" ]]; then
      version="$version*"
    fi
  fi

  echo_info "Basis-Image wird aktualisiert: $base_image"
  devbox_docker pull "$base_image"

  local tag="$devbox_image:$version_tag"
  echo_info "Baue Devbox-Image: $tag"
  devbox_docker build \
    --build-arg DEVBOX_BASE_IMAGE="$base_image" \
    --build-arg DEVBOX_VERSION="$version" \
    --tag "$tag" \
    ./docker
}

build "$@"
