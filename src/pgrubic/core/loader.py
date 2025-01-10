"""Methods to load rules and formatters."""

from __future__ import annotations

import os
import typing
import fnmatch
import inspect
import importlib

from pgrubic import (
    RULES_DIRECTORY,
    RULES_BASE_MODULE,
    FORMATTERS_DIRECTORY,
    FORMATTERS_BASE_MODULE,
)
from pgrubic.core import config, linter


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
