"""Entry point."""

import sys
import fnmatch
from collections import abc

from pgshield import core
from pgshield.core import docs_generator


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    loaded_config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=loaded_config)

    formatter: core.Formatter = core.Formatter()

    loaded_rules: list[core.Checker] = core.load_rules()

    # Add only seleted and not ignored rules
    for rule in loaded_rules:

        if (
            not loaded_config.select
            or any(
                fnmatch.fnmatch(rule.code, pattern) for pattern in loaded_config.select
            )
        ) and not any(
            fnmatch.fnmatch(rule.code, pattern) for pattern in loaded_config.ignore
        ):

            linter.checkers.add(rule())

    total_violations: int = 0

    # Add only included and not excluded files
    for source_path in source_paths:

        if (
            not loaded_config.include
            or any(
                fnmatch.fnmatch(source_path, pattern)
                for pattern in loaded_config.include
            )
        ) and not any(
            fnmatch.fnmatch(source_path, pattern) for pattern in loaded_config.exclude
        ):

            # formatter.diff(source_path=source_path)

            violations: int = linter.run(source_path)

            total_violations += violations

    if total_violations > 0:

        sys.stdout.write(
            f"Found {total_violations} violations.\n",
        )

        sys.exit(1)


if __name__ == "__main__":
    cli()
