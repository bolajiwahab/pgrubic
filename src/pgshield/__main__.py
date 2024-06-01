"""Entry point."""

import sys
import pathlib
from collections import abc

from pgshield import utils, config, rules_directories
from pgshield import linter as _linter


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    linter: _linter.Linter = _linter.Linter()

    loaded_rules: list[_linter.Checker] = utils.load_rules(rules_directories)

    loaded_codes: list[str] = [rule.code for rule in loaded_rules]

    utils.check_duplicate_rules(loaded_rules)

    loaded_config = config.load_config(
        pathlib.Path(
            "/Users/bolajiwahab/repos/bolajiwahab/pgshield/src/pgshield/.pgshield",
        ),
    )

    for rule in loaded_rules:

        if rule.code in loaded_config.get(
            "lint.select", loaded_codes,
        ) and rule.code not in loaded_config.get("lint.ignore", []):

            linter.checkers.add(rule())

    for source_path in source_paths:
        linter.run(source_path)


if __name__ == "__main__":
    cli()
