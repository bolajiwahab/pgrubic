"""Entry point."""

import sys
from collections import abc

from pgshield.core import config, loader
from pgshield.core import linter as _linter
from pgshield.core import formatter as _formatter


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    loaded_config = config.parse_config()

    linter: _linter.Linter = _linter.Linter(config=loaded_config)

    formatter: _formatter.Formatter = _formatter.Formatter()

    loaded_rules: list[_linter.Checker] = loader.load_rules()

    for rule in loaded_rules:

        if (
            not loaded_config.select or rule.code in loaded_config.select
        ) and rule.code not in loaded_config.ignore:

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
