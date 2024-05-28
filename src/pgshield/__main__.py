"""Entry point."""

import sys
from collections import abc

from pgshield import utils, rules_directories
from pgshield import linter as _linter


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    linter: _linter.Linter = _linter.Linter()

    loaded_rules: list[_linter.Checker] = utils.load_rules(rules_directories)

    utils.check_duplicate_rules(loaded_rules)

    for rule in loaded_rules:
        linter.checkers.add(rule())

    for source_path in source_paths:
        linter.run(source_path)


if __name__ == "__main__":
    cli()
