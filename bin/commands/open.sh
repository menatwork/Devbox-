load_dotenv_or_die DEVBOX_PROJECTS_DIR

set -x

p="${PWD#$DEVBOX_PROJECTS_DIR}"

if [[ "$p" == "" || "$p" == "$PWD" ]]; then
  echo_error "$PWD ist kein Projektverzeichnis."
  exit 1
fi

p="$PWD"

while [[ "$(dirname "$p")" != "$DEVBOX_PROJECTS_DIR" ]]; do
  p="$(dirname "$p")"
done

project="$(basename "$p")"
url="http://$project.devbox.localhost"

case "$(uname)" in
  Linux) xdg-open "$url" ;;
  Darwin) open "$url" ;;
  *)
    echo_error "Kann auf diesem Betriebssystem keine URLs öffnen."
    exit 1
esac
