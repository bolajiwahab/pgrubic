"""Utilities."""

import typing
import inspect
import importlib

from pglast import ast  # type: ignore[import-untyped]

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
    """Hack to get statement location and the raw statement from ancestors.

    This is due to the way ancestors are represented in the AST tree,
    which is not a list by default hence we can't use list functions
    such as len directly.
    """
    nodes: list[str] = []

    for node in ancestors:

        if node is None:
            break

        nodes.append(node)

    # We need to go two steps back to locate our current node's statement.
    return len(nodes) - 2
