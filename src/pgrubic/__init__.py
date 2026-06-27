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

REPOSITORY_URL: typing.Final[str] = "https://github.com/bolajiwahab/pgrubic"

ISSUES_URL: typing.Final[str] = f"{REPOSITORY_URL}/issues"

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


def get_fully_qualified_name(node: tuple[ast.String] | ast.String) -> str:
    """Get fully qualified name.

    Parameters:
    ----------
    node: tuple[ast.Node]
        Node to get fully qualified name for.

    Returns:
    -------
    str
        Fully qualified name.

    """
    if isinstance(node, ast.String):
        return str(node.sval)

    return ".".join(n.sval for n in node if n.sval is not None)


@enum.unique
class Operators(enum.StrEnum):
    """Operators."""

    EQ = "="
    NOT_EQ = "<>"


def is_non_volatile_function(
    *,
    function: ast.FuncCall,
    non_volatile_functions: list[str],
) -> bool:
    """Check if function is non volatile.

    Parameters:
    ----------
    function: ast.Node
        Function to check.

    Returns:
    -------
    bool
        True if function is non volatile, False otherwise.

    """
    function_name = function.funcname

    # Use pg_catalog if function is not schema qualified.
    if function_name and len(function_name) == 1:
        function_name = (ast.String(sval="pg_catalog"), *function_name)

    return (
        isinstance(function, ast.FuncCall)
        and function.funcname
        and get_fully_qualified_name(function.funcname) in non_volatile_functions
    )
