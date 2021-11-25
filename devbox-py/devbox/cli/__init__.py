from dataclasses import dataclass

from ..config import Config


class Error(Exception):
    """
    Base error type for CLI errors.
    """
    pass


@dataclass
class Context(object):
    args: 'list[str]'
    config: Config
    repo_dir: str