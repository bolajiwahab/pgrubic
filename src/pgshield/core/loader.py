"""Method to load rules."""

import typing
import inspect
import pathlib
import importlib

from pgshield.core import errors, linter

module_path = pathlib.Path("pgshield/rules/")


def load_rules() -> list[linter.Checker]:
    """Load rules."""
    rules: list[linter.Checker] = []

    for path in module_path.glob("**/[!_]*.py"):

        module = importlib.import_module(str(path).replace(".py", "").replace("/", "."))

        for _, obj in inspect.getmembers(
            module,
            lambda x: inspect.isclass(x)
            and x.__module__ == module.__name__,  # noqa: B023
        ):

            # remove private classes
            if issubclass(obj, linter.Checker) and not obj.__name__.startswith("_"):

                rules.append(typing.cast(linter.Checker, obj))

                _set_locations_for_node(obj)

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


def _set_locations_for_node(obj: typing.Any) -> None:
    """Set locations for node in visitors."""
    for name, method in inspect.getmembers(obj, inspect.isfunction):

        if method.__name__.startswith("visit_"):

            setattr(obj, name, linter.set_locations_for_node(method))
