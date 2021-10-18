# just in case we're not in the devbox repo
cd "$devbox_src_dir"

image_tag=latest
devbox_version="$image_tag"

if [[ $# != 1 ]]; then
  echo_info "No version given; will tag with ':latest'"
  echo_info "To create a versioned release build, run this command with a version argument"
elif ! git tag --points-at HEAD | grep --quiet "^$1$"; then
  echo_error "Tried to build release for version $1, but no such tag points at HEAD."
  echo_error "To tag a release build, HEAD must have a matching version tag."
  exit 1
else
  echo_info "Building release image for version $1"
  image_tag="$1"
fi

if [[ "$devbox_version" == latest ]]; then
  devbox_version="$(git rev-parse --short HEAD)"

  if [[ $(git diff --stat) != "" ]]; then
    devbox_version="$devbox_version*"
  fi
fi

docker_args=(
  build

  --build-arg DEVBOX_VERSION="$devbox_version"
  --tag "$devbox_image:$image_tag"

  ./docker
)

devbox_docker "${docker_args[@]}"
