"""Method to generate docs for rules."""

import typing
import inspect
import importlib
import pathlib

from pgshield import RULE_DIRECTORIES
from pgshield.core import noqa, errors, linter, load_rules

base_path = pathlib.Path(__file__).parent.absolute()

current_directory = pathlib.Path.cwd()

rules = load_rules()

for rule in rules:

    with pathlib.Path.open(base_path / f"{rule.__name__}.md", "w") as file:

        file.write(f"## {rule.__name__}\n\n")
# def load_rules() -> list[linter.Checker]:
#     """Load rules."""
#     rules: list[linter.Checker] = []

#     for directory in RULE_DIRECTORIES:

#         module = importlib.import_module(directory)

#         for _, obj in inspect.getmembers(module, inspect.isclass):

#             if issubclass(obj, linter.Checker) and not obj.__name__.startswith("_"):

#                 rules.append(typing.cast(linter.Checker, obj))

#                 # These are decorators and they are executed inner --> outer
#                 _apply_noqa(obj)
#                 _set_locations_for_node(obj)

#     _check_duplicate_rules(rules)

#     return rules