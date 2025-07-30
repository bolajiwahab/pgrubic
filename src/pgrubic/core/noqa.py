"""Handling noqa comments."""

import sys
import typing
import pathlib
import dataclasses

from pglast import parser
from colorama import Fore, Style

from pgrubic import PACKAGE_NAME

A_STAR: typing.Final[str] = "*"
ASCII_SEMI_COLON: typing.Final[str] = "ASCII_59"
ASCII_OPEN_PARENTHESIS: typing.Final[str] = "ASCII_40"
ASCII_CLOSE_PARENTHESIS: typing.Final[str] = "ASCII_41"
SQL_COMMENT: typing.Final[str] = "SQL_COMMENT"
C_COMMENT: typing.Final[str] = "C_COMMENT"
BEGIN_BLOCK: typing.Final[str] = "BEGIN_P"
END_BLOCK: typing.Final[str] = "END_P"

LINT_IGNORE_DIRECTIVE: typing.Final[str] = "noqa"
FORMAT_IGNORE_DIRECTIVE: typing.Final[str] = "fmt"
SEMI_COLON: typing.Final[str] = ";"
NEW_LINE: typing.Final[str] = "\n"
SPACE: typing.Final[str] = " "


class Token(typing.NamedTuple):
    """Representation of a token."""

    start: int
    end: int
    name: str
    kind: str


class Statement(typing.NamedTuple):
    """Representation of an SQL statement."""

    start_location: int
    end_location: int
    text: str


def extract_statements(
    *,
    source_code: str,
) -> list[Statement]:
    """Extract statements from source code.

    Parameters:
    ----------
    source_code: str
        Source code to extract statements from.

    Returns:
    -------
    list[Statement]
        List of statements.
    """
    statements: list[Statement] = []

    statement_start_location = 0

    tokens: list[Token] = parser.scan(source_code)

    inside_block = False  # Tracks if we are inside BEGIN ... END block

    inside_parenthesis = False  # Tracks if we are inside parentheses (...)

    for token in tokens:
        if token.name == BEGIN_BLOCK:
            inside_block = True

        if inside_block and token.name == END_BLOCK:
            inside_block = False  # Function block ends

        if token.name == ASCII_OPEN_PARENTHESIS:
            inside_parenthesis = True

        if token.name == ASCII_CLOSE_PARENTHESIS:
            inside_parenthesis = False  # Parenthesis ends

        # Check if we have reached a semi-colon or the end of the source code
        if token.name == ASCII_SEMI_COLON or token is tokens[-1]:
            if not (inside_block or inside_parenthesis):
                # In order to include the last character, we need to increase the end
                # location by 1
                actual_end_location = token.end + 1
                locations.append(
                    Statement(
                        start_location=statement_start_location,
                        end_location=actual_end_location,
                        text=(source_code[statement_start_location:actual_end_location]),
                    ),
                )
                # Move to the next statement
                statement_start_location = actual_end_location + 1
            else:
                continue
    return statements


def _get_lint_rules_from_comment(
    comment: str,
    location: int,
    section: str,
) -> list[str]:
    """Get lint rules from comment.

    Parameters:
    ----------
    comment: str
        The comment.

    location: int
        Location of comment.

    section: str
        Section of comment.

    Returns:
    -------
    list[str]
        List of lint rules.
    """
    comment_remainder = comment.removeprefix(section)

    if not comment_remainder:
        return [A_STAR]

    rules: list[str] = [
        rule.strip()
        for rule in comment_remainder.removeprefix(":").split(",")
        if rule and comment_remainder.startswith(":")
    ]

    if not rules:
        sys.stderr.write(
            f"{Fore.YELLOW}Warning: Malformed `{LINT_IGNORE_DIRECTIVE}` directive at location {location}. Expected `{LINT_IGNORE_DIRECTIVE}: <rules>`{Style.RESET_ALL}{NEW_LINE}",  # noqa: E501
        )

    return rules


@dataclasses.dataclass(kw_only=True)
class NoQaDirective:
    """Representation of a noqa directive."""

    source_file: str | None = None
    location: int
    line_number: int
    column_offset: int
    rule: str
    used: bool = False


def extract_statement_lint_ignores(
    *,
    statement: Statement,
    source_code: str,
) -> list[NoQaDirective]:
    """Extract lint ignores from SQL statement.

    Parameters:
    ----------
    statement: Statement
        Statement to extract lint ignores from.

    source_code: str
        Source code to construct the line number and column offset of lint ignores from.

    Returns:
    -------
    list[NoQaDirective]
        List of lint ignores.
    """
    statement_lint_ignores: list[NoQaDirective] = []

    for token in typing.cast(list[Token], parser.scan(statement.text)):
        if token.name == SQL_COMMENT:
            actual_start_location = statement.start_location + token.start

            line_number = source_code[:actual_start_location].count(NEW_LINE) + 1

            # Here, we extract last comment because we can have a comment followed
            # by another comment e.g -- new table -- noqa: US005
            comment = (
                # In order to include the last character, we need to increase the end
                # location by 1
                statement.text[token.start : (token.end + 1)].split("--")[-1].strip()
            )

            if comment.startswith(LINT_IGNORE_DIRECTIVE):
                rules = _get_lint_rules_from_comment(
                    comment,
                    token.start,
                    LINT_IGNORE_DIRECTIVE,
                )

                statement_lint_ignores.extend(
                    NoQaDirective(
                        location=statement.start_location,
                        line_number=line_number,
                        # Calculate column offset as the position within the line where
                        # our directive starts
                        column_offset=(
                            actual_start_location
                            - source_code.rfind(NEW_LINE, 0, actual_start_location)
                        ),
                        rule=rule,
                    )
                    for rule in rules
                )

    return statement_lint_ignores


def extract_file_lint_ignores(
    *,
    source_file: str,
    source_code: str,
) -> list[NoQaDirective]:
    """Extract lint ignores from the start of a source file.

    Parameters:
    ----------
    source_file: str
        The source file.

    source_code: str
        Source code to extract lint ignores from.

    Returns:
    -------
    list[NoQaDirective]
        List of lint ignores.
    """
    file_ignores: list[NoQaDirective] = []

    for token in typing.cast(list[Token], parser.scan(source_code)):
        if token.start == 0 and token.name == SQL_COMMENT:
            # In order to include the last character, we need to increase the end
            # location by one
            actual_end_location = token.end + 1

            comment = (
                source_code[token.start : actual_end_location].split("--")[-1].strip()
            )

            if comment.startswith(f"{PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}"):
                rules = _get_lint_rules_from_comment(
                    comment,
                    token.start,
                    section=f"{PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}",
                )

                file_ignores.extend(
                    NoQaDirective(
                        source_file=source_file,
                        location=token.start,
                        line_number=1,
                        column_offset=1,
                        rule=rule,
                    )
                    for rule in rules
                )
        else:
            break

    return file_ignores


def check_file_format_skip(
    *,
    source_code: str,
) -> bool:
    """Check if formatting should be skipped for source code.

    Parameters:
    ----------
    source_code: str
        Source code to check file format skip for.

    Returns:
    -------
    bool
        True if format skip is found, False otherwise.
    """
    for token in typing.cast(list[Token], parser.scan(source_code)):
        if token.start == 0 and token.name == SQL_COMMENT:
            # In order to include the last character, we need to increase the end
            # location by one
            actual_end_location = token.end + 1

            comment = (
                source_code[token.start : actual_end_location].split("--")[-1].strip()
            )

            return bool(
                comment.startswith(f"{PACKAGE_NAME}: {FORMAT_IGNORE_DIRECTIVE}")
                and comment.removeprefix(f"{PACKAGE_NAME}: {FORMAT_IGNORE_DIRECTIVE}")
                .removeprefix(":")
                .strip()
                == "skip",
            )

    return False


def _check_statement_format_skip(
    *,
    statement: Statement,
) -> bool:
    """Check if formatting should be skipped for SQL statement.

    Parameters:
    ----------
    statement: Statement
        Statement to check if formatting should be skipped.

    Returns:
    -------
    bool
        True if format skip is found, False otherwise.
    """
    for token in typing.cast(list[Token], parser.scan(statement.text)):
        if token.name == SQL_COMMENT:
            # In order to include the last character, we need to increase the end
            # location by one
            actual_end_location = token.end + 1

            comment = (
                statement.text[token.start : actual_end_location].split("--")[-1].strip()
            )

            if (
                comment.startswith(FORMAT_IGNORE_DIRECTIVE)
                and comment.removeprefix(FORMAT_IGNORE_DIRECTIVE)
                .removeprefix(":")
                .strip()
                == "skip"
            ):
                return True

    return False


def check_statement_format_skip(
    *,
    source_code: str,
    statement: Statement,
) -> bool:
    """Check if formatting should be skipped for SQL statement base on source code or the
    statement.

    Parameters:
    ----------
    statement: Statement
        Statement to check if formatting should be skipped.

    Returns:
    -------
    bool
        True if format skip is found, False otherwise.
    """
    return check_file_format_skip(
        source_code=source_code,
    ) or _check_statement_format_skip(statement=statement)


class Comment(typing.NamedTuple):
    """Representation of an SQL comment."""

    location: int
    text: str
    at_start_of_line: bool
    continue_previous: bool


def extract_comments(*, statement: Statement) -> list[Comment]:
    """Extract comments from SQL statement.

    Parameters:
    ----------
    statement: Statement
        Statement to extract comments from.

    Returns:
    -------
    list[Comment]
        List of comments.
    """
    comments: list[Comment] = []
    # We have consciously decided to always have comments at the top of the
    # respective statement
    continue_previous = True

    for token in parser.scan(statement.text):
        if token.name in (C_COMMENT, SQL_COMMENT):
            comment = statement.text[token.start : (token.end + 1)]
            comments.append(
                Comment(
                    location=0,
                    text=comment,
                    at_start_of_line=True,
                    continue_previous=continue_previous,
                ),
            )
    return comments


def report_unused_lint_ignores(
    *,
    source_file: str,
    lint_ignores: list[NoQaDirective],
) -> None:
    """Get unused ignores.

    Parameters:
    ----------
    source_file: str
        Path to the source file.

    lint_ignores: list[NoQaDirective]
        List of noqa directives.

    Returns:
    -------
    None
    """
    for ignore in lint_ignores:
        if not ignore.used:
            sys.stdout.write(
                f"{source_file}:{ignore.line_number}:{ignore.column_offset}:"
                f" {Fore.YELLOW}Unused {LINT_IGNORE_DIRECTIVE} directive{Style.RESET_ALL}"
                f" (unused: {Fore.RED}{Style.BRIGHT}{ignore.rule}{Style.RESET_ALL}){NEW_LINE}",  # noqa: E501
            )


def add_file_level_general_lint_ignore(sources: set[pathlib.Path]) -> int:
    """Add file-level general lint ignore to the beginning of each source.

    Parameters:
    ----------
    sources: set[pathlib.Path]
        Set of source files.

    Returns:
    -------
    int
        Number of sources modified.
    """
    sources_modified = 0

    for source in sources:
        skip = False
        source_code = source.read_text()

        for token in typing.cast(list[Token], parser.scan(source_code)):
            if token.start == 0 and token.name == SQL_COMMENT:
                # In order to include the last character, we need to increase the end
                # location by one
                actual_end_location = token.end + 1

                comment = (
                    source_code[token.start : actual_end_location].split("--")[-1].strip()
                )

                if comment == f"{PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}":
                    skip = True
                    break

        if not skip:
            source.write_text(
                f"-- {PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}\n{source_code}",
            )
            sources_modified += 1
            continue

    return sources_modified
