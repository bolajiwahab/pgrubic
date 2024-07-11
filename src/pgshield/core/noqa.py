"""Handling noqa comments."""

import re
import typing
import functools
from collections import abc

from pglast import ast, parser

from pgshield.core import errors


def remove_delimiter_from_sql_comment(statement: str, delimter: str = ";") -> str:
    """Remove delimiter from SQL statement."""
    comment_pattern = r"\s*--.*|^\s*\/[*][\S\s]*?[*]\/"
    return re.sub(
        comment_pattern,
        lambda match: match.group(0).replace(delimter, ""),
        statement,
        flags=re.MULTILINE,
    )


def _split_statement_into_lines(statement: str) -> list[tuple[int, int]]:
    """Split SQL statement into lines."""
    lines: list[tuple[int, int]] = []
    line_offset = 0

    for line in statement.split(";"):

        line_length = len(line)
        lines.append((line_offset, line_offset + line_length))
        line_offset += line_length + 1

    return lines


def extract(statement: str) -> list[tuple[int, str]]:
    """Extract noqa from inline SQL comment."""
    lines = _split_statement_into_lines(statement)

    comments: list[tuple[int, str]] = []

    for token in parser.scan(statement):

        msg = f"Malformed 'noqa' section in line {token.start}. Expected 'noqa: <rule>"
        if token.name == "IDENT":
            print(statement[token.start:token.end+1])

        if token.name == "SQL_COMMENT":

            for beginning_of_line_offset, end_of_line_offset in lines:
                if beginning_of_line_offset <= token.start < end_of_line_offset:
                    break

            comment = statement[token.start : (token.end + 1)]

            # Normal comment lines can also have noqa e.g. --new table -- noqa: UNS05
            # Therefore extract last possible inline ignore.
            comment = [c.strip() for c in comment.split("--")][-1]

            if comment.startswith("noqa"):
                # This is an ignore identifier
                comment_remainder = comment[4:]

                if comment_remainder:

                    if not comment_remainder.startswith(":"):
                        raise errors.SQLParseError(
                            msg,
                        )

                    comment_remainder = comment_remainder[1:].strip()

                [
                    comments.append((beginning_of_line_offset, rule.strip()))  # type: ignore[func-returns-value]
                    for rule in comment_remainder.split(",")
                ]

    return comments


def apply(func: abc.Callable[..., typing.Any]) -> abc.Callable[..., typing.Any]:
    """Apply noqa on rules."""

    @functools.wraps(func)
    def wrapper(
        self: typing.Any,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> typing.Any:

        if (
            self.statement_location,
            self.code,
        ) in self.noqa_ignore_rules or (
            self.statement_location,
            "*",
        ) in self.noqa_ignore_rules:

            return None

        return func(self, ancestors, node)

    return wrapper
