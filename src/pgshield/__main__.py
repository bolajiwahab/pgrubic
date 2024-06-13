"""Entry point."""

import sys
from collections import abc

from pgshield import core


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    loaded_config = core.parse_config()

    linter: core.Linter = core.Linter(config=loaded_config)

    formatter: core.Formatter = core.Formatter()

    loaded_rules: list[core.Checker] = core.load_rules()

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
