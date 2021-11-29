mkdir /run/devbox

p=(
  git
  htop
  less
  openssh-client
  rsync
  runit
  vim
)

build-helper update
build-helper upgrade
build-helper install "${p[@]}"
