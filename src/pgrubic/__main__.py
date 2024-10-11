"""Entry point."""

import sys
import pathlib
from collections import abc

from pgrubic import core


def cli(config: core.Config, argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    linter: core.Linter = core.Linter(config=config)

    core.BaseChecker.config = config

    rules: list[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    violations: core.ViolationMetric = core.ViolationMetric()

    source_paths = core.filter_source_paths(source_paths=source_paths, config=config)

    for source_path in source_paths:
        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:
            source_code: str = source_file.read()

        _violations: core.ViolationMetric = linter.run(
            source_path=pathlib.Path(source_path),
            source_code=source_code,
        )

        violations.total += _violations.total
        violations.fixed_total += _violations.fixed_total
        violations.fixable_auto_total += _violations.fixable_auto_total
        violations.fixable_manual_total += _violations.fixable_manual_total

    if violations.total > 0:
        if config.lint.fix is True:
            sys.stdout.write(
                f"Found {violations.total} violations"
                f" ({violations.fixed_total} fixed,"
                f" {violations.fixable_manual_total} remaining).\n",
            )

        else:
            sys.stdout.write(
                f"Found {violations.total} violations.\n"
                f"{violations.fixable_auto_total} fixes available.\n",
            )

        sys.exit(1)


if __name__ == "__main__":
    config: core.Config = core.parse_config()

    cli(config=config)
