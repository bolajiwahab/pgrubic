"""Method to load rules."""

import typing
import inspect
import importlib

from pgshield import RULE_DIRECTORIES
from pgshield.core import noqa, errors, linter

import pathlib
module_path = pathlib.Path("pgshield/rules/")

# print(module_path)

# for path in module_path.glob("**/*.py"):
#     module = importlib.import_module(str(path).replace(".py", "").replace("/", "."))
#     print(module)


def load_rules() -> list[linter.Checker]:
    """Load rules."""
    rules: list[linter.Checker] = []

    for path in module_path.glob("**/*.py"):

        module = importlib.import_module(str(path).replace(".py", "").replace("/", "."))
        # print(dir(module.__path__))
        # print(inspect.getmembers(module, inspect.isclass))


        for _, obj in inspect.getmembers(module, inspect.isclass):

            if issubclass(obj, linter.Checker) and not obj.__name__.startswith("_"):

                rules.append(typing.cast(linter.Checker, obj))

                # These are decorators and they are executed inner --> outer
                _apply_noqa(obj)
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


def _apply_noqa(obj: typing.Any) -> None:
    """Apply noqa on visitors."""
    for name, method in inspect.getmembers(obj, inspect.isfunction):

        if method.__name__.startswith("visit_"):

            setattr(obj, name, noqa.apply(method))


def _set_locations_for_node(obj: typing.Any) -> None:
    """Set locations for node in visitors."""
    for name, method in inspect.getmembers(obj, inspect.isfunction):

        if method.__name__.startswith("visit_"):

            setattr(obj, name, linter.set_locations_for_node(method))
