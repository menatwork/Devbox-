import logging
import os
import sys


LEVEL_COLORS = {
    logging.CRITICAL: '\x1b[31m',
    logging.ERROR: '\x1b[31m',
    logging.WARNING: '\x1b[33m',
    logging.INFO: '\x1b[34m',
    logging.DEBUG: '\x1b[36m',
}


COLOR_RESET = '\x1b[0m'


class CliFormatter(logging.Formatter):

    def __init__(self, use_colors=True) -> None:
        self.use_colors = use_colors
        super().__init__(fmt='[devbox] %(levelname)s: %(msg)s')

    def format(self, record) -> str:
        color = self.getLevelColor(record.levelno)
        color_reset = self.getResetColor()
        s = logging.Formatter.format(self, record)
        s = f'{color}{s}{color_reset}'
        return s

    def getLevelColor(self, levelno) -> str:
        if not self.use_colors:
            return ''
        return LEVEL_COLORS[levelno]

    def getResetColor(self):
        if not self.use_colors:
            return ''
        return COLOR_RESET


def init():
    use_colors = 'NO_COLOR' not in os.environ

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(CliFormatter(use_colors))

    logging.basicConfig(level=logging.DEBUG, handlers=[handler])

