"""pgrubic."""

import typing
import pathlib

from pglast import ast

PROGRAM_NAME: str = "pgrubic"

RULES_BASE_MODULE: str = f"{PROGRAM_NAME}/rules/"

RULES_DIRECTORY: pathlib.Path = pathlib.Path(__file__).resolve().parent / "rules/"

CONFIG_FILE: str = f"{PROGRAM_NAME}.toml"

DEFAULT_CONFIG: pathlib.Path = pathlib.Path(__file__).resolve().parent / CONFIG_FILE


def get_full_qualified_name(node: tuple[typing.Any]) -> str:
    """Get fully qualified type name."""
    if isinstance(node, ast.String):
        return str(node.sval)

    return ".".join(n.sval for n in node)
