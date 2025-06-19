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
BEGIN_BLOCK: typing.Final[str] = "BEGIN_P"
END_BLOCK: typing.Final[str] = "END_P"
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
    locations: list[Statement] = []

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

        if token.name == ASCII_SEMI_COLON or token is tokens[-1]:
            if not (inside_block or inside_parenthesis):
                # For ASCII_SEMI_COLON, both start and end locations are the same and
                # in order to still have it in the statement, we need to increase the end
                # location by one
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
    return locations


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


def _get_statement_locations(
    locations: list[Statement],
    stop: int,
) -> tuple[int, int]:
    """Get statement start and end locations.

    Parameters:
    ----------
    locations: list[Statement]
        List of statements.

    stop: int
        Stop location.

    Returns:
    -------
    tuple[int, int]
        Statement start and end locations.
    """
    for statement_start_location, statement_end_location, _ in locations:
        if statement_start_location <= stop < statement_end_location:
            break

    return statement_start_location, statement_end_location


@dataclasses.dataclass(kw_only=True)
class NoQaDirective:
    """Representation of a noqa directive."""

    source_file: str | None = None
    location: int
    line_number: int
    column_offset: int
    rule: str
    used: bool = False


LINT_IGNORE_DIRECTIVE: typing.Final[str] = "noqa"


def _extract_statement_lint_ignores(
    source_code: str,
    statements: list[Statement],
) -> list[NoQaDirective]:
    """Extract lint ignores from SQL statements.

    Parameters:
    ----------
    source_code: str
        Source code to extract lint ignores from.

    statements: list[Statement]
        List of statements.

    Returns:
    -------
    list[NoQaDirective]
        List of lint ignores.
    """
    statement_lint_ignores: list[NoQaDirective] = []

    for token in typing.cast(list[Token], parser.scan(source_code)):
        if token.name == "SQL_COMMENT":
            statement_start_location, statement_end_location = _get_statement_locations(
                statements,
                token.start,
            )

            line_number = source_code[:statement_end_location].count(NEW_LINE) + 1

            # Here, we extract last comment because we can have a comment followed
            # by another comment e.g -- new table -- noqa: US005
            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if comment.startswith(LINT_IGNORE_DIRECTIVE):
                rules = _get_lint_rules_from_comment(
                    comment,
                    token.start,
                    LINT_IGNORE_DIRECTIVE,
                )

                statement_lint_ignores.extend(
                    NoQaDirective(
                        location=statement_start_location,
                        line_number=line_number,
                        column_offset=(statement_end_location - token.start),
                        rule=rule,
                    )
                    for rule in rules
                )

    return statement_lint_ignores


def _extract_file_lint_ignores(
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

    for token in parser.scan(source_code):
        if token.start == 0 and token.name == "SQL_COMMENT":
            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if comment.strip().startswith(f"{PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}"):
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
                        column_offset=0,
                        rule=rule,
                    )
                    for rule in rules
                )
        else:
            break

    return file_ignores


def extract_lint_ignores(
    *,
    source_file: str,
    source_code: str,
    statements: list[Statement],
) -> list[NoQaDirective]:
    """Extract lint ignores from source code.

    Parameters:
    ----------
    source_file: str
        The source file.

    source_code: str
        Source code to extract lint ignores from.

    statements: list[Statement]
        List of statements.

    Returns:
    -------
    list[NoQaDirective]
        List of ignores.
    """
    return _extract_statement_lint_ignores(
        source_code=source_code,
        statements=statements,
    ) + _extract_file_lint_ignores(
        source_file=source_file,
        source_code=source_code,
    )


def extract_statement_format_ignores(
    source_code: str,
    statements: list[Statement],
) -> list[int]:
    """Extract format ignores from SQL statements.

    Parameters:
    ----------
    source_code: str
        Source code to extract ignores from.

    statements: list[Statement]
        List of statements.

    Returns:
    -------
    list[int]
        List of ignores.
    """
    statement_format_ignores: list[int] = []

    for token in parser.scan(source_code):
        if token.name == "SQL_COMMENT":
            statement_start_location, _ = _get_statement_locations(
                statements,
                token.start,
            )

            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if (
                comment.strip().startswith("fmt")
                and comment.removeprefix("fmt").removeprefix(":").strip() == "skip"
            ):
                statement_format_ignores.append(
                    statement_start_location,
                )

    return statement_format_ignores


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
    statement: str
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
        if token.name in ("C_COMMENT", "SQL_COMMENT"):
            comment = statement.text[token.start : (token.end + 1)]
            at_start_of_line = not statement.text[
                : token.start - statement.start_location
            ]
            comments.append(
                Comment(
                    0,
                    comment,
                    at_start_of_line,
                    continue_previous,
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


def add_file_level_general_ignore(sources: set[pathlib.Path]) -> int:
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
            if token.start == 0 and token.name == "SQL_COMMENT":
                comment = (
                    source_code[token.start : (token.end + 1)].split("--")[-1].strip()
                )

                if comment.strip() == f"{PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}":
                    skip = True
                    break

        if not skip:
            source.write_text(
                f"-- {PACKAGE_NAME}: {LINT_IGNORE_DIRECTIVE}\n{source_code}",
            )
            sources_modified += 1
            continue

    return sources_modified
