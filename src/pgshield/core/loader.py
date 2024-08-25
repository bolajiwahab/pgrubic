"""Method to load rules."""

import typing
import inspect
import functools
import importlib
from collections import abc

from pglast import ast, visitors

from pgshield import RULES_DIRECTORY, RULES_BASE_MODULE
from pgshield.core import linter


def load_rules() -> list[linter.BaseChecker]:
    """Load rules."""
    rules: list[linter.BaseChecker] = []

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
            if issubclass(rule, linter.BaseChecker) and not rule.__name__.startswith(
                "_",
            ):

                # set rule code
                rule.code = rule.__module__.split(".")[-1]

                rules.append(typing.cast(linter.BaseChecker, rule))

                _add_set_locations_to_rule(rule)

                _add_apply_fix_to_rule(rule)

    return rules


def _add_set_locations_to_rule(node: typing.Any) -> None:
    """Add _set_locations to rule."""
    for name, method in inspect.getmembers(node, inspect.isfunction):

        if method.__name__.startswith("visit_"):

            setattr(node, name, _set_locations(method))


def _add_apply_fix_to_rule(node: typing.Any) -> None:
    """Add apply_fix to rule."""
    for name, method in inspect.getmembers(node, inspect.isfunction):

        if method.__name__.startswith("_fix"):

            setattr(node, name, apply_fix(method))


def _set_locations(
    func: abc.Callable[..., typing.Any],
) -> abc.Callable[..., typing.Any]:
    """Set locations for node."""
    # merge _set_locations and _get_line_details of linter

    @functools.wraps(func)
    def wrapper(
        self: linter.BaseChecker,
        ancestors: visitors.Ancestor,
        node: ast.Node,
    ) -> typing.Any:

        node_location = getattr(node, "location", 0)

        self.node_location = node_location if node_location else 0

        self.statement_location = ancestors.find_nearest(ast.RawStmt).node.stmt_location

        self.statement_length = ancestors.find_nearest(ast.RawStmt).node.stmt_len

        return func(self, ancestors, node)

    return wrapper


def apply_fix(
    func: abc.Callable[..., typing.Any],
) -> abc.Callable[..., typing.Any]:
    """Apply fix only if it is applicable."""

    @functools.wraps(func)
    def wrapper(
        self: linter.BaseChecker,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Any:

        if not self.is_fix_applicable:

            return None

        return func(self, *args, **kwargs)

    return wrapper
