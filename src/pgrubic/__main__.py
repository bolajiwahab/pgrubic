"""Entry point."""

import sys
import fnmatch
import pathlib
from collections import abc

from pgrubic import core


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    core.BaseChecker.config = config

    loaded_rules: list[core.BaseChecker] = core.load_rules()

    # Add only selected and not ignored rules
    for rule in loaded_rules:

        if (
            not config.lint.select
            or any(
                fnmatch.fnmatch(rule.code, pattern) for pattern in config.lint.select
            )
        ) and not any(
            fnmatch.fnmatch(rule.code, pattern) for pattern in config.lint.ignore
        ):

            linter.checkers.add(rule())

    violations: core.ViolationMetric = core.ViolationMetric()

    for source_path in source_paths:

        # Run lint on only included and not excluded files
        if (
            not config.lint.include
            or any(
                fnmatch.fnmatch(source_path, pattern) for pattern in config.lint.include
            )
        ) and not any(
            fnmatch.fnmatch(source_path, pattern) for pattern in config.lint.exclude
        ):

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

    cli()
