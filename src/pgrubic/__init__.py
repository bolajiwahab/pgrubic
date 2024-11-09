"""pgrubic."""

import enum
import typing
import pathlib

from pglast import ast

PROGRAM_NAME: str = "pgrubic"

DOCUMENTATION_URL: str = "https://bolajiwahab.github.io/pgrubic"

RULES_BASE_MODULE: str = f"{PROGRAM_NAME}/rules/"

FORMATTERS_BASE_MODULE: str = f"{PROGRAM_NAME}/formatters/"

PARENT_DIRECTORY: pathlib.Path = pathlib.Path(__file__).resolve().parent

RULES_DIRECTORY: pathlib.Path = PARENT_DIRECTORY / "rules/"

FORMATTERS_DIRECTORY: pathlib.Path = PARENT_DIRECTORY / "formatters/"

CONFIG_FILE: str = f"{PROGRAM_NAME}.toml"

DEFAULT_CONFIG: pathlib.Path = pathlib.Path(__file__).resolve().parent / CONFIG_FILE

CONFIG_PATH_ENVIRONMENT_VARIABLE: str = f"{PROGRAM_NAME.upper()}_CONFIG_PATH"


def get_full_qualified_name(node: tuple[typing.Any]) -> str:
    """Get fully qualified type name."""
    if isinstance(node, ast.String):
        return str(node.sval)

    return ".".join(n.sval for n in node)


@enum.unique
class Operators(enum.StrEnum):
    """Operators."""

    EQ = "="
    NOT_EQ = "<>"
