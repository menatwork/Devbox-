# just in case we're not in the devbox repo
cd "$devbox_src_dir"

if [[ $# != 1 ]]; then
  echo_info "No version given; will tag with ':latest'"
  echo_info "To create a versioned release build, run this command with a version argument"
  image_tag="latest"
elif ! git tag --points-at HEAD | grep --quiet "^$1$"; then
  echo_error "Tried to build release for version $1, but no such tag points at HEAD."
  echo_error "To tag a release build, HEAD must have a matching version tag."
  exit 1
else
  echo_info "Building release image for version $1"
  image_tag="$1"
fi

docker_args=(
  build

  --build-arg DEVBOX_UID="$(id -u)"
  --build-arg DEVBOX_GID="$(id -g)"

  --tag "$devbox_image:$image_tag"

  ./docker
)

devbox_docker "${docker_args[@]}"
