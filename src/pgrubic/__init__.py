"""pgrubic."""

import enum
import typing
import pathlib
import tomllib
import importlib.metadata

from pglast import ast

PACKAGE_NAME: typing.Final[str] = "pgrubic"

WORKERS_ENVIRONMENT_VARIABLE: typing.Final[str] = f"{PACKAGE_NAME.upper()}_WORKERS"

DEFAULT_WORKERS: typing.Final[int] = 4

DOCUMENTATION_URL: typing.Final[str] = "https://bolajiwahab.github.io/pgrubic"

PACKAGE_DIRECTORY: typing.Final[pathlib.Path] = pathlib.Path(__file__).resolve().parent

SOURCE_DIRECTORY: typing.Final[pathlib.Path] = PACKAGE_DIRECTORY.parent

PROJECT_DIRECTORY: typing.Final[pathlib.Path] = SOURCE_DIRECTORY.parent

RULES_DIRECTORY: typing.Final[pathlib.Path] = PACKAGE_DIRECTORY / "rules/"

FORMATTERS_DIRECTORY: typing.Final[pathlib.Path] = PACKAGE_DIRECTORY / "formatters/"

pyproject_file = pathlib.Path(PROJECT_DIRECTORY / "pyproject.toml")
if pyproject_file.exists():
    with pathlib.Path(PROJECT_DIRECTORY / "pyproject.toml").open("rb") as f:
        pyproject_config = tomllib.load(f)
        __version__: str = pyproject_config["project"]["version"]
else:
    __version__ = importlib.metadata.version(PACKAGE_NAME)  # pragma: no cover

RULES_BASE_MODULE: typing.Final[str] = f"{PACKAGE_NAME}/rules/"

FORMATTERS_BASE_MODULE: typing.Final[str] = f"{PACKAGE_NAME}/formatters/"


def get_fully_qualified_name(node: tuple[typing.Any]) -> str:
    """Get fully qualified type name."""
    if isinstance(node, ast.String):
        return str(node.sval)

    return ".".join(n.sval for n in node)


@enum.unique
class Operators(enum.StrEnum):
    """Operators."""

    EQ = "="
    NOT_EQ = "<>"
