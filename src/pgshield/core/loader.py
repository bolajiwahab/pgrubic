"""Method to load rules."""

import typing
import inspect
import functools
import importlib
from collections import abc

from pglast import ast

from pgshield import RULES_DIRECTORY, RULES_BASE_MODULE
from pgshield.core import linter


def load_rules() -> list[linter.Checker]:
    """Load rules."""
    rules: list[linter.Checker] = []

    for path in sorted(RULES_DIRECTORY.rglob("[!_]*.py"), key=lambda x: x.name):

        module = importlib.import_module(
            str(RULES_BASE_MODULE / path.relative_to(RULES_DIRECTORY))
            .replace(".py", "")
            .replace("/", "."),
        )

        for _, rule in inspect.getmembers(
            module,
            lambda x: inspect.isclass(x)
            and x.__module__ == module.__name__,  # noqa: B023
        ):

            # skip private classes
            if issubclass(rule, linter.Checker) and not rule.__name__.startswith("_"):

                # set rule code
                rule.code = rule.__module__.split(".")[-1]

                rules.append(typing.cast(linter.Checker, rule))

                _set_locations_for_node(rule)

    return rules


def _set_locations_for_node(node: typing.Any) -> None:
    """Set locations for node in visitors."""
    for name, method in inspect.getmembers(node, inspect.isfunction):

        if method.__name__.startswith("visit_"):

            setattr(node, name, set_locations_for_node(method))


def set_locations_for_node(
    func: abc.Callable[..., typing.Any],
) -> abc.Callable[..., typing.Any]:
    """Set locations for node."""
    # merge set_locations_for_node and _get_line_details of linter

    @functools.wraps(func)
    def wrapper(
        self: linter.Checker,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> typing.Any:

        node_location = getattr(node, "location", 0)

        self.node_location = node_location if node_location else 0

        self.statement_location = ancestors.find_nearest(ast.RawStmt).node.stmt_location

        self.statement_length = ancestors.find_nearest(ast.RawStmt).node.stmt_len

        return func(self, ancestors, node)

    return wrapper
