"""
Devbox schema files (.devbox.yml)
"""


class SchemaError(Exception):
    pass


from .schema import *  # noqa: E402
