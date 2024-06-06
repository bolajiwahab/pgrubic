"""Entry point."""

import sys
import pathlib
from collections import abc

from pgshield import utils, config, rules_directories
from pgshield import linter as _linter
from pgshield import formatter as _formatter


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    loaded_config = config.load_config(
        pathlib.Path(
            "/Users/bolajiwahab/repos/bolajiwahab/pgshield/src/pgshield/.pgshield",
        ),
    )

    linter: _linter.Linter = _linter.Linter(config=loaded_config)

    formatter: _formatter.Formatter = _formatter.Formatter()

    loaded_rules: list[_linter.Checker] = utils.load_rules(rules_directories)

    loaded_codes: list[str] = [rule.code for rule in loaded_rules]

    utils.check_duplicate_rules(loaded_rules)

    for rule in loaded_rules:

        if rule.code in loaded_config.get(
            "lint.select", loaded_codes,
        ) and rule.code not in loaded_config.get("lint.ignore", []):

            linter.checkers.add(rule())

    violations_found: list[bool] = []

    for source_path in source_paths:

        # formatter.diff(source_path=source_path)

        result: bool = linter.run(source_path)

        violations_found.append(result)

    if any(violations_found):

        sys.exit(1)


if __name__ == "__main__":
    cli()
