import docker  # type: ignore[import]


def ensure_devbox_network_exists() -> None:
    client = docker.DockerClient()
    try:
        client.networks.get('devbox')
    except docker.errors.NotFound:
        client.networks.create('devbox')