"""Method to generate docs for rules."""

import sys
import pathlib

from caseconverter import kebabcase

from pgshield.core.loader import load_rules

# base_path: pathlib.Path = pathlib.Path(
#     "/Users/bolajiwahab/repos/bolajiwahab/pgshield/docs/docs/rules",
# )

base_path = pathlib.Path.cwd() / "docs/rules"

rules = load_rules()

for rule in rules:

    with pathlib.Path.open(
        base_path / rule.name.split(".")[0] / f"{kebabcase(rule.__name__)}.md", "w",
    ) as file:

        file.write(f"# {kebabcase(rule.__name__)} ({rule.code})\n\n")

        file.write(f"{rule.name.split(".")[0]}({rule.code})\n\n")

        file.write(f"::: {sys.modules[rule.__module__].__name__}.{rule.__name__}\n\n")
