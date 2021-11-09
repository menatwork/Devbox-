p=(
  python3-cerberus
  python3-docker
  python3-jinja2
  python3-pip
  python3-yaml
)

build-helper install  "${p[@]}"
pip3 install -e /src/devbox-py
