"""Genrate documentation for rules."""

import sys
import shutil
import pathlib

from caseconverter import kebabcase

from pgrubic.core.loader import load_rules

rules_path = pathlib.Path.cwd() / "docs/docs/rules"

rules = load_rules()

shutil.rmtree(rules_path)

for rule in rules:

    group = rule.__module__.split(".")[-2]

    pathlib.Path(rules_path / group).mkdir(parents=True, exist_ok=True)

    with pathlib.Path.open(
        rules_path / group / f"{kebabcase(rule.__name__)}.md",
        "w",
    ) as file:

        file.write(f"# {kebabcase(rule.__name__)} ({rule.code})\n\n")

        if rule.is_auto_fixable is True:
            file.write("Automatic fix is available\n\n")
        else:
            file.write("Automatic fix is not available\n\n")

        file.write(f"::: {sys.modules[rule.__module__].__name__}.{rule.__name__}\n")