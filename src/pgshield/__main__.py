"""Entry point."""

import sys
import fnmatch
import pathlib
from collections import abc

from pgshield import core


def cli(argv: abc.Sequence[str] = sys.argv) -> None:
    """CLI."""
    source_paths: abc.Sequence[str] = argv[1:]

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    core.Checker.config = config

    formatter: core.Formatter = core.Formatter()

    loaded_rules: list[core.Checker] = core.load_rules()

    # Add only selected and not ignored rules
    for rule in loaded_rules:

        if (
            not config.select
            or any(fnmatch.fnmatch(rule.code, pattern) for pattern in config.select)
        ) and not any(fnmatch.fnmatch(rule.code, pattern) for pattern in config.ignore):

            linter.checkers.add(rule())

    violations: core.ViolationMetric = core.ViolationMetric()

    for source_path in source_paths:

        # Run lint on only included and not excluded files
        if (
            not config.include
            or any(fnmatch.fnmatch(source_path, pattern) for pattern in config.include)
        ) and not any(
            fnmatch.fnmatch(source_path, pattern) for pattern in config.exclude
        ):

            with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:

                source_code: str = source_file.read()

            # formatter.diff(source_path=source_path)

            _violations: core.ViolationMetric = linter.run(
                source_path=pathlib.Path(source_path),
                source_code=source_code,
            )

            violations.violations_total += _violations.violations_total
            violations.violations_fixed_total += _violations.violations_fixed_total
            violations.violations_fixable_auto_total += (
                _violations.violations_fixable_auto_total
            )
            violations.violations_fixable_manual_total += (
                _violations.violations_fixable_manual_total
            )

    if violations.violations_total > 0:

        if config.fix is True:

            sys.stdout.write(
                f"Found {violations.violations_total} violations"
                f" ({violations.violations_fixed_total} fixed,"
                f" {violations.violations_fixable_manual_total} remaining).\n",
            )

        else:
            sys.stdout.write(
                f"Found {violations.violations_total} violations.\n"
                f"{violations.violations_fixable_auto_total} fixes available.\n",
            )

        sys.exit(1)


if __name__ == "__main__":
    cli()
