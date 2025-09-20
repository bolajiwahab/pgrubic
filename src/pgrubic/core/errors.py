"""pgrubic errors."""

import sys
import typing

from colorama import Fore, Style

from pgrubic.core import noqa


class BaseError(Exception):
    """Base class for all exceptions."""


class MissingConfigError(BaseError):
    """Raised when a config is missing."""


class ConfigFileNotFoundError(BaseError):
    """Raised when a config file is not found."""


class ConfigParseError(BaseError):
    """Raised when a config file cannot be parsed."""


class Error(typing.NamedTuple):
    """Representation of an error."""

    source_file: str
    source_code: str
    statement_start_location: int
    statement_end_location: int
    statement: str
    message: str
    hint: str


def print_errors(
    *,
    errors: set[Error],
    source_file: str,
) -> None:
    """Print all errors collected during linting.

    Parameters:
    ----------
    errors: set[errors.Error]
        Errors to print.
    source_file: str
        Path to the source file.

    Returns:
    -------
    None
    """
    for error in errors:
        sys.stdout.write(
            f"{noqa.NEW_LINE}{source_file}: {error.message}: {error.hint}{noqa.NEW_LINE}",
        )

        line_number = (
            error.source_code[: error.statement_end_location].count(noqa.NEW_LINE) + 1
        )

        for idx, line in enumerate(
            error.statement.splitlines(keepends=False),
            start=line_number - error.statement.count(noqa.NEW_LINE),
        ):
            sys.stdout.write(
                f"{Fore.BLUE}{idx} | {Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}{noqa.NEW_LINE}",  # noqa: E501
            )
