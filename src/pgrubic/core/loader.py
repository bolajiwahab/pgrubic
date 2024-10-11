"""Method to load rules."""

import typing
import fnmatch
import inspect
import functools
import importlib
from collections import abc

from pglast import ast, visitors

from pgrubic import RULES_DIRECTORY, RULES_BASE_MODULE
from pgrubic.core import config, linter


def load_rules(config: config.Config) -> list[linter.BaseChecker]:
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
            lambda x: inspect.isclass(x) and x.__module__ == module.__name__,  # noqa: B023
        ):
            if (
                issubclass(rule, linter.BaseChecker)
                and not rule.__name__.startswith(
                    "_",
                )
                and (
                    not config.lint.select
                    or any(
                        fnmatch.fnmatch(rule.code, pattern)
                        for pattern in config.lint.select
                    )
                )
                and not any(
                    fnmatch.fnmatch(rule.code, pattern) for pattern in config.lint.ignore
                )
            ):
                rules.append(typing.cast(linter.BaseChecker, rule))

                add_set_locations_to_rule(rule)

                add_apply_fix_to_rule(rule)

    return rules


def add_set_locations_to_rule(node: typing.Any) -> None:
    """Add _set_locations to rule."""
    for name, method in inspect.getmembers(node, inspect.isfunction):
        if method.__name__.startswith("visit_"):
            setattr(node, name, _set_locations(method))


def add_apply_fix_to_rule(node: typing.Any) -> None:
    """Add apply_fix to rule."""
    for name, method in inspect.getmembers(node, inspect.isfunction):
        if method.__name__.startswith("_fix"):
            setattr(node, name, apply_fix(method))


def _set_locations(
    func: abc.Callable[..., typing.Any],
) -> abc.Callable[..., typing.Any]:
    """Set locations for node."""

    @functools.wraps(func)
    def wrapper(
        self: linter.BaseChecker,
        ancestors: visitors.Ancestor,
        node: ast.Node,
    ) -> typing.Any:
        node_location = getattr(node, "location", 0)
        # Some nodes have location as None.
        node_location = node_location if node_location else 0

        statement_location = ancestors.find_nearest(ast.RawStmt).node.stmt_location
        statement_length = ancestors.find_nearest(ast.RawStmt).node.stmt_len

        column_offset = (
            node_location - statement_location
            if isinstance(node_location, int) and node_location > 0
            else statement_length
        )

        statement_location_end = statement_location + statement_length

        line_number = self.source_code[:statement_location_end].count("\n") + 1

        line_start = self.source_code[:statement_location_end].rfind(";\n") + 1

        line_end = self.source_code.find("\n", statement_location_end)

        source_text = self.source_code[line_start:line_end].strip("\n")

        self.line_number = line_number
        self.column_offset = column_offset
        self.source_text = source_text
        self.statement_location = statement_location

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
