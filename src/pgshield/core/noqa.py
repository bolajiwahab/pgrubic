"""Handling noqa comments."""

import re

from pglast import parser

from pgshield.core import errors


def remove_delimiter_from_sql_comment(source_code: str, delimter: str = ";") -> str:
    """Remove delimiter from SQL comment."""
    comment_pattern = r"\s*--.*|^\s*\/[*][\S\s]*?[*]\/"
    return re.sub(
        comment_pattern,
        lambda match: match.group(0).replace(delimter, ""),
        source_code,
        flags=re.MULTILINE,
    )


def _build_start_end_locations(source_code: str) -> list[tuple[int, int]]:
    """Build start and end locations."""
    locations: list[tuple[int, int]] = []

    start_location = 0

    for statement in source_code.split(";"):

        statement_length = len(statement)
        locations.append((start_location, start_location + statement_length))
        start_location += statement_length + 1

    return locations


def _get_rules_from_inline_comment(comment: str, location: int) -> list[str]:
    """Get rule from inline comment."""
    msg = f"Malformed 'noqa' section in line {location}. Expected 'noqa: <rule>'"
    # Normal comment lines can also have noqa e.g. --new table -- noqa: UN005
    # Therefore extract last possible inline ignore.
    comment = [c.strip() for c in comment.split("--")][-1]

    rules: list[str] = []

    if comment.startswith("noqa"):
        # This is an ignore identifier
        comment_remainder = comment[4:]

        if comment_remainder:

            if not comment_remainder.startswith(":"):
                raise errors.SQLParseError(
                    msg,
                )

            rules = comment_remainder[1:].strip().split(",")

    return rules


def _get_start_location(locations: list[tuple[int, int]], stop: int) -> int:
    """Get start location."""
    for start_location, end_location in locations:

        if start_location <= stop < end_location:

            break

    return start_location


def extract(source_code: str) -> list[tuple[int, str]]:
    """Extract noqa from inline SQL comment."""
    locations = _build_start_end_locations(source_code)

    inline_ignores: list[tuple[int, str]] = []

    for token in parser.scan(source_code):

        if token.name == "SQL_COMMENT":

            start_location = _get_start_location(locations, token.start)

            comment = source_code[token.start : (token.end + 1)]

            rules = _get_rules_from_inline_comment(comment, token.start)

            if rules:
                [
                    inline_ignores.append((start_location, rule))  # type: ignore[func-returns-value]
                    for rule in rules
                ]

    return inline_ignores
