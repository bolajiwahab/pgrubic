"""Handling noqa comments."""
import re

from pglast import parser  # type: ignore[import-untyped]

from pgshield.core import errors


def extract(statement: str) -> list[tuple[int, str]]:
    """Extract noqa from inline SQL comment."""
    lines: list[tuple[int, int, str]] = []
    line_offset = 0

    statement = re.sub(
        r"^\s*--.*\n?|^\s*\/[*][\S\s]*?[*]\/", "", statement, flags=re.MULTILINE,
    )

    for line in statement.split(";"):

        line_length = len(line)
        lines.append((line_offset, line_offset + line_length, line))
        line_offset += line_length + 1

    comments: list[tuple[int, str]] = []

    for token in parser.scan(statement):

        msg = f"Malformed 'noqa' section in line {token.start}. Expected 'noqa: <rule>"

        if token.name == "SQL_COMMENT":

            for beginning_of_line_offset, end_of_line_offset, _ in lines:
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
