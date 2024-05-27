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
