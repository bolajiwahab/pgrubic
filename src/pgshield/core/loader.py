"""Method to load rules."""

import typing
import inspect
import importlib

from pgshield import rule_directories
from pgshield.core import errors, linter


def load_rules(directories: list[str] = rule_directories) -> list[linter.Checker]:
    """Load rules."""
    rules: list[linter.Checker] = []

    for directory in directories:

        module = importlib.import_module(directory)

        for _, obj in inspect.getmembers(module, inspect.isclass):

            if issubclass(obj, linter.Checker) and not obj.__name__.startswith("_"):

                rules.append(typing.cast(linter.Checker, obj))

    _check_duplicate_rules(rules)

    return rules


def _check_duplicate_rules(rules: list[linter.Checker]) -> None:
    """Check for duplicate rules."""
    seen: set[str] = set()

    for rule in rules:

        if rule.name in seen or rule.code in seen:

            raise errors.DuplicateRuleDetectedError((rule.name, rule.code))

        seen.add(rule.name)
        seen.add(rule.code)
