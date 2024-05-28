"""Utilities."""

import re
import typing
import inspect
import importlib

from pglast import ast, parser  # type: ignore[import-untyped]

from pgshield import errors, linter


def load_rules(directories: list[str]) -> list[linter.Checker]:
    """Load rules."""
    rules: list[linter.Checker] = []

    for directory in directories:

        module = importlib.import_module(directory)

        for _, obj in inspect.getmembers(module, inspect.isclass):

            if (
                issubclass(obj, linter.Checker)
            ):

                rules.append(typing.cast(linter.Checker, obj))

    return rules


def check_duplicate_rules(rules: list[linter.Checker]) -> None:
    """Check for duplicate rules."""
    seen: set[str] = set()

    for rule in rules:

        # if any(var in seen for var in seen):
        if rule.name in seen or rule.code in seen:

            raise errors.DuplicateRuleDetectedError((rule.name, rule.code))

        seen.add(rule.name)
        seen.add(rule.code)


def get_statement_index(ancestors: ast.Node) -> int:
    """Get statement index.

    pglast's AST is not a python list hence we cannot use list functions such as `len`
    directly on it. We need to build a list from the AST.
    """
    nodes: list[str] = []

    for node in ancestors:

        if node is None:
            break

        nodes.append(node)

    # The current visitor's Node is located two indexes from the end of the list.
    return len(nodes) - 2


def extract_noqa(statement: str) -> list[tuple[int, str]]:
    """Extract noqa from inline SQL comment."""
    lines: list[tuple[int, int, str]] = []
    line_offset = 0

    statement = re.sub(r"^\s*--.*\n?", " ", statement, flags=re.MULTILINE)

    for line in statement.split(";"):

        line_length = len(line)
        lines.append((line_offset, line_offset + line_length, line))
        line_offset += (line_length + 1)

    comments: list[tuple[int, str]] = []

    for token in parser.scan(statement):

        msg = f"Malformed 'noqa' section in line {token.start}. Expected 'noqa: <rule>"

        if token.name == "SQL_COMMENT":

            for beginning_of_line_offset, end_of_line_offset, _ in lines:
                if beginning_of_line_offset <= token.start < end_of_line_offset:
                    break

            comment = statement[token.start:(token.end + 1)]
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

                comments.append((beginning_of_line_offset, comment_remainder))

    return comments
