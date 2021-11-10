p=(
  # required by some npm packages
  build-essential
  nodejs
  python2
  python3
)

build-helper update
build-helper install "${p[@]}"

npm install -g yarn
