from dataclasses import dataclass
import logging
import os


class ConfigError(Exception):
    pass


@dataclass
class Config(object):
    projects_dir: str
    projects_volume: str
    debug: bool


def load_dotenv_config(path: str) -> Config:
    data = {}
    did_error = False

    with open(path) as f:
        for line in f:
            line = line.strip()

            if line == '' or line.startswith('#'):
                continue

            bits = line.split('=', maxsplit=1)

            if len(bits) != 2:
                logging.error(f"Kann Zeile in .env nicht parsen: {line}")
                did_error = True

            k, v = bits
            data[k] = v

    if did_error:
        raise ConfigError()

    projects_dir = os.path.normpath(data['DEVBOX_PROJECTS_DIR'])
    projects_volume = data.get('DEVBOX_PROJECTS_VOLUME', projects_dir)
    debug = data.get('DEVBOX_CLI_DEBUG') == '1'

    return Config(
        projects_dir=projects_dir,
        projects_volume=projects_volume,
        debug=debug,
    )
