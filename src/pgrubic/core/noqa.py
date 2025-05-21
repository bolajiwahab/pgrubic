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
SEMI_COLON: typing.Final[str] = ";"
NEW_LINE: typing.Final[str] = "\n"
SPACE: typing.Final[str] = " "


class Statement(typing.NamedTuple):
    """Representation of an SQL statement."""

    start_location: int
    end_location: int
    text: str


def extract_statement_locations(
    *,
    source_code: str,
) -> list[Statement]:
    """Build statements start and end locations.

    Parameters:
    ----------
    source_code: str
        Source code to extract statements from.

    Returns:
    -------
    list[Statement]
        List of statements.

    Raises:
    ------
    MissingStatementTerminatorError
        If semicolon is missing at the end of a statement.
    """
    locations: list[Statement] = []

    statement_start_location = 0

    # Add semi-colon at the end if missing
    if not source_code.rstrip(NEW_LINE).rstrip(SPACE).endswith(SEMI_COLON):
        source_code += SEMI_COLON

    tokens = parser.scan(source_code)

    inside_block = False  # Tracks if we are inside BEGIN ... END block

    for _, token in enumerate(tokens):
        # Detect BEGIN
        if token.name == "BEGIN_P":
            inside_block = True

        # Detect END
        if inside_block and token.name == "END_P":
            inside_block = False  # Function block ends

        # Detect open parenthesis
        if token.name == "ASCII_40":
            inside_parenthesis = True

        # Detect close parenthesis
        if token.name == "ASCII_41":
            inside_parenthesis = False  # Parenthesis ends

        if token.name == ASCII_SEMI_COLON:
            if not (inside_block or inside_parenthesis):
                locations.append(
                    Statement(
                        start_location=statement_start_location,
                        end_location=token.end,
                        text=(
                            source_code[statement_start_location : token.end] + SEMI_COLON
                        ).strip(),
                    ),
                )
                statement_start_location = token.end + 1
            else:
                continue
    return locations


def _get_rules_from_inline_comment(
    comment: str,
    location: int,
    section: str = "noqa",
) -> list[str]:
    """Get rules from inline comment.

    Parameters:
    ----------
    comment: str
        Inline comment.
    location: int
        Location of inline comment.
    section: str
        Section of inline comment.

    Returns:
    -------
    list[str]
        List of rules.
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
            f"{Fore.YELLOW}Warning: Malformed `noqa` directive at location {location}. Expected `noqa: <rules>`{Style.RESET_ALL}\n",  # noqa: E501
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


def _extract_statement_ignores(
    source_code: str,
) -> list[NoQaDirective]:
    """Extract ignores from SQL statements.

    Parameters:
    ----------
    source_code: str
        Source code to extract ignores from.

    Returns:
    -------
    list[NoQaDirective]
        List of ignores.
    """
    locations = extract_statement_locations(
        source_code=source_code,
    )

    inline_ignores: list[NoQaDirective] = []

    for token in parser.scan(source_code):
        if token.name == "SQL_COMMENT":
            statement_start_location, statement_end_location = _get_statement_locations(
                locations,
                token.start,
            )

            line_number = source_code[:statement_end_location].count("\n") + 1

            # Here, we extract last comment because we can have a comment followed
            # by another comment e.g -- new table -- noqa: US005
            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if comment.startswith("noqa"):
                rules = _get_rules_from_inline_comment(comment, token.start)

                inline_ignores.extend(
                    NoQaDirective(
                        location=statement_start_location,
                        line_number=line_number,
                        column_offset=(statement_end_location - token.start),
                        rule=rule,
                    )
                    for rule in rules
                )

    return inline_ignores


def _extract_file_ignore(*, source_file: str, source_code: str) -> list[NoQaDirective]:
    """Extract ignore from the start of a source file.

    Parameters:
    ----------
    source_file: str
        Path to the source file.
    source_code: str
        Source code to extract ignores from.

    Returns:
    -------
    list[NoQaDirective]
        List of ignores.
    """
    file_ignores: list[NoQaDirective] = []

    for token in parser.scan(source_code):
        if token.start == 0 and token.name == "SQL_COMMENT":
            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if comment.strip().startswith(f"{PACKAGE_NAME}: noqa"):
                rules = _get_rules_from_inline_comment(
                    comment,
                    token.start,
                    section=f"{PACKAGE_NAME}: noqa",
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


def extract_ignores(*, source_file: str, source_code: str) -> list[NoQaDirective]:
    """Extract ignores from source code.

    Parameters:
    ----------
    source_file: str
        Path to the source file.
    source_code: str
        Source code to extract ignores from.

    Returns:
    -------
    list[NoQaDirective]
        List of ignores.
    """
    return _extract_statement_ignores(
        source_code=source_code,
    ) + _extract_file_ignore(
        source_file=source_file,
        source_code=source_code,
    )


def extract_format_ignores(source_code: str) -> list[int]:
    """Extract format ignores from SQL statements.

    Parameters:
    ----------
    source_code: str
        Source code to extract ignores from.

    Returns:
    -------
    list[int]
        List of ignores.
    """
    locations = extract_statement_locations(
        source_code=source_code,
    )

    inline_ignores: list[int] = []

    for token in parser.scan(source_code):
        if token.name == "SQL_COMMENT":
            statement_start_location, _ = _get_statement_locations(
                locations,
                token.start,
            )

            comment = source_code[token.start : (token.end + 1)].split("--")[-1].strip()

            if (
                comment.strip().startswith("fmt")
                and comment.removeprefix("fmt").removeprefix(":").strip() == "skip"
            ):
                inline_ignores.append(
                    statement_start_location,
                )

    return inline_ignores


class Comment(typing.NamedTuple):
    """Representation of an SQL comment."""

    location: int
    text: str
    at_start_of_line: bool
    continue_previous: bool


def extract_comments(*, source_code: str) -> list[Comment]:
    """Extract comments from SQL statements.

    Parameters:
    ----------
    source_code: str
        Source code to extract comments from.

    Returns:
    -------
    list[Comment]
        List of comments.
    """
    locations = extract_statement_locations(
        source_code=source_code,
    )

    comments: list[Comment] = []
    continue_previous = False

    for token in parser.scan(source_code):
        if token.name in ("C_COMMENT", "SQL_COMMENT"):
            statement_start_location, _ = _get_statement_locations(
                locations,
                token.start,
            )

            comment = source_code[token.start : (token.end + 1)]
            at_start_of_line = not source_code[
                : token.start - statement_start_location
            ].strip()
            comments.append(
                Comment(
                    statement_start_location,
                    comment,
                    at_start_of_line,
                    continue_previous,
                ),
            )
            continue_previous = True
        else:
            continue_previous = False
    return comments


def report_unused_ignores(
    *,
    source_file: str,
    inline_ignores: list[NoQaDirective],
) -> None:
    """Get unused ignores.

    Parameters:
    ----------
    source_file: str
        Path to the source file.
    inline_ignores: list[NoQaDirective]
        Inline noqa directives.

    Returns:
    -------
    None
    """
    for ignore in inline_ignores:
        if not ignore.used:
            sys.stdout.write(
                f"{source_file}:{ignore.line_number}:{ignore.column_offset}:"
                f" {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL}"
                f" (unused: {Fore.RED}{Style.BRIGHT}{ignore.rule}{Style.RESET_ALL})\n",
            )


def add_file_level_general_ignore(sources: set[pathlib.Path]) -> int:
    """Add file-level general noqa directive to the begining of each source.

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

        for token in parser.scan(source_code):
            if token.start == 0 and token.name == "SQL_COMMENT":
                comment = (
                    source_code[token.start : (token.end + 1)].split("--")[-1].strip()
                )

                if comment.strip() == f"{PACKAGE_NAME}: noqa":
                    skip = True
                    break

        if not skip:
            source.write_text(f"-- {PACKAGE_NAME}: noqa\n{source_code}")
            sources_modified += 1
            continue

    return sources_modified
