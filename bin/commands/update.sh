echo_info "Repository $devbox_src_dir wird aktualisiert..."
git -C "$devbox_src_dir" pull

echo
echo_info "Neuestes Devbox-Image wird bezogen..."
devbox_docker image pull "$devbox_image:latest"

#if devbox_is_running; then
#  devbox_info "Restarting container..."
#  docker restart "$devbox_container"
#else
#  devbox_info "Container seems to be down, not restarting"
#fi

devbox_info "Und fertig."
