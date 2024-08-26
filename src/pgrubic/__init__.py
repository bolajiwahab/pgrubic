"""pgrubic."""

import typing
import pathlib

PROGRAM_NAME: str = "pgrubic"

RULES_BASE_MODULE: str = f"{PROGRAM_NAME}/rules/"

RULES_DIRECTORY: pathlib.Path = pathlib.Path(__file__).resolve().parent / "rules/"

CONFIG_FILE: str = f"{PROGRAM_NAME}.toml"

DEFAULT_CONFIG: pathlib.Path = pathlib.Path(__file__).resolve().parent / CONFIG_FILE


def get_full_qualified_type_name(node: tuple[typing.Any]) -> str:
    """Get fully qualified type name."""
    return ".".join(n.sval for n in node)
