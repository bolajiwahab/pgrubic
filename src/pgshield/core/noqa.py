"""Handling noqa comments."""

import re
import sys
import dataclasses

from pglast import parser
from colorama import Fore, Style

from pgshield.core import errors


def _remove_delimiter_from_comments(source_code: str, delimiter: str = ";") -> str:
    """Remove delimiter from SQL comments."""
    comment_pattern = r"\s*--.*|^\s*\/[*][\S\s]*?[*]\/"

    return re.sub(
        comment_pattern,
        lambda match: match.group(0).replace(delimiter, ""),
        source_code,
        flags=re.MULTILINE,
    )


def _build_statements_start_end_locations(
    source_code: str,
    delimiter: str = ";",
) -> list[tuple[int, int]]:
    """Build statements start and end locations."""
    locations: list[tuple[int, int]] = []

    statement_start_location = 0

    for statement in source_code.split(delimiter):

        statement_length = len(statement)

        locations.append(
            (statement_start_location, statement_start_location + statement_length),
        )

        statement_start_location += statement_length + 1

    return locations


def _get_rules_from_inline_comment(comment: str, location: int) -> list[str]:
    """Get rule from inline comment."""
    msg = f"Malformed 'noqa' section in line {location}. Expected 'noqa: <rule>'"

    rules: list[str] = []

    # This is an ignore identifier e.g noqa: UN005
    comment_remainder = comment[4:]

    if comment_remainder:

        if not comment_remainder.startswith(":"):

            raise errors.SQLParseError(
                msg,
            )

        rules = comment_remainder[1:].replace(",", "").split()

    return rules


def _get_statement_locations(
    locations: list[tuple[int, int]], stop: int,
) -> tuple[int, int]:
    """Get statement start and end locations."""
    for statement_start_location, statement_end_location in locations:

        if statement_start_location <= stop < statement_end_location:

            break

    return statement_start_location, statement_end_location


@dataclasses.dataclass(kw_only=True)
class NoQaDirective:
    """Representation of a noqa directive."""

    location: int
    line_number: int
    column_offset: int
    rules: list[str]
    used: bool = False


def extract_ignores_from_inline_comments(
    source_code: str,
) -> list[NoQaDirective]:
    """Extract ignores from inline SQL comments."""
    source_code = _remove_delimiter_from_comments(source_code)

    locations = _build_statements_start_end_locations(source_code)

    inline_ignores: list[NoQaDirective] = []

    for token in parser.scan(source_code):

        if token.name == "SQL_COMMENT":

            statement_start_location, statement_end_location = _get_statement_locations(
                locations,
                token.start,
            )

            line_number = source_code[:statement_end_location].count("\n") + 1

            comment = source_code[token.start : (token.end + 1)]

            # Usual comments can contain noqa e.g. --new table -- noqa: UN005
            # Hence we extract last possible noqa.
            comment = [c.strip() for c in comment.split("--")][-1]

            if comment.startswith("noqa"):

                rules = _get_rules_from_inline_comment(comment, token.start)

                inline_ignores.append(
                    NoQaDirective(
                        location=statement_start_location,
                        line_number=line_number,
                        column_offset=(statement_end_location - token.start),
                        rules=rules,
                    ),
                )

    return inline_ignores


def report_unused_ignores(
    *,
    file_name: str,
    inline_ignores: list[NoQaDirective],
) -> None:
    """Get unused ignores."""
    for ignore in inline_ignores:

        if not ignore.used:

            for rule in ignore.rules:

                sys.stdout.write(
                    f"{file_name}:{ignore.line_number}:{ignore.column_offset}:"
                    f" {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL}"
                    f" (unused: {Fore.RED}{Style.BRIGHT}{rule}{Style.RESET_ALL})\n",
                )
