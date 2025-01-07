"""Methods to load rules and formatters."""

from __future__ import annotations

import os
import typing
import fnmatch
import inspect
import functools
import importlib

from pgrubic import (
    RULES_DIRECTORY,
    RULES_BASE_MODULE,
    FORMATTERS_DIRECTORY,
    FORMATTERS_BASE_MODULE,
)
from pgrubic.core import noqa, config, linter

if typing.TYPE_CHECKING:
    from collections import abc  # pragma: no cover

    from pglast import ast, visitors  # pragma: no cover


def load_rules(config: config.Config) -> set[linter.BaseChecker]:
    """Load rules."""
    rules: set[linter.BaseChecker] = set()

    for path in sorted(RULES_DIRECTORY.rglob("[!_]*.py"), key=lambda x: x.name):
        module = importlib.import_module(
            str(RULES_BASE_MODULE / path.relative_to(RULES_DIRECTORY))
            .replace(".py", "")
            .replace(os.path.sep, "."),
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
                        fnmatch.fnmatch(rule.code, pattern + "*")
                        for pattern in config.lint.select
                    )
                )
                and not any(
                    fnmatch.fnmatch(rule.code, pattern + "*")
                    for pattern in config.lint.ignore
                )
            ):
                rules.add(rule)

                add_set_locations_to_rule(rule)

                add_apply_fix_to_rule(rule)

    return rules


def load_formatters() -> set[typing.Callable[[], None]]:
    """Load formatters."""
    formatters: set[typing.Callable[[], None]] = set()

    for path in sorted(FORMATTERS_DIRECTORY.rglob("[!_]*.py"), key=lambda x: x.name):
        module = importlib.import_module(
            str(FORMATTERS_BASE_MODULE / path.relative_to(FORMATTERS_DIRECTORY))
            .replace(".py", "")
            .replace(os.path.sep, "."),
        )

        for _, formatter in inspect.getmembers(
            module,
            lambda x: inspect.isfunction(x)
            and x.__name__.endswith("_stmt")
            and x.__module__ == module.__name__,  # noqa: B023
        ):
            formatters.add(formatter)

    return formatters


def add_set_locations_to_rule(rule: linter.BaseChecker) -> None:
    """Add _set_locations to rule."""
    for name, method in inspect.getmembers(rule, inspect.isfunction):
        if method.__name__.startswith("visit_"):
            setattr(rule, name, _set_locations(method))


def add_apply_fix_to_rule(rule: linter.BaseChecker) -> None:
    """Add apply_fix to rule."""
    for name, method in inspect.getmembers(rule, inspect.isfunction):
        if method.__name__.startswith("_fix"):
            setattr(rule, name, apply_fix(method))


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
        # some nodes have location attribute which is different from node location
        # for example ast.CreateTablespaceStmt while some nodes do not carry location.
        if hasattr(node, "location") and isinstance(node.location, int):
            self.node_location = self.statement_location + node.location
        else:
            self.node_location = self.statement_location + len(self.statement)

        # get the position of the newline just before our node location,
        line_start = self.source_code.rfind(noqa.NEW_LINE, 0, self.node_location) + 1
        # get the position of the newline just after our node location
        line_end = self.source_code.find(noqa.NEW_LINE, self.node_location)

        # line number is number of newlines before our node location,
        # increment by 1 to land on the actual node
        self.line_number = self.source_code[: self.node_location].count(noqa.NEW_LINE) + 1
        self.column_offset = self.node_location - line_start + 1

        # If a node has no location, we return the whole statement instead
        if hasattr(node, "location") and isinstance(node.location, int):
            self.line = self.source_code[line_start:line_end]
        else:
            self.line = self.statement.strip()

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
        if not self.config.lint.fix:
            return None

        if not self.is_fix_applicable:
            return None

        return func(self, *args, **kwargs)

    return wrapper
