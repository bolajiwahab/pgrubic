"""Entry point."""

import sys
import pathlib

import click

from pgrubic import PROGRAM_NAME, core


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog=f"""
Examples:\n
   {PROGRAM_NAME} lint .\n
   {PROGRAM_NAME} lint *.sql\n
   {PROGRAM_NAME} lint example.sql\n
   {PROGRAM_NAME} format src/queries\n
""",
)
@click.version_option()
def cli() -> None:
    """Pgrubic: PostgreSQL linter for schema migrations and design best practices."""


@cli.command()
@click.option("--fix", is_flag=True, help="Fix lint violations automatically.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def lint(paths: tuple[pathlib.Path, ...], *, fix: bool) -> None:
    """Lint SQL files."""
    config: core.Config = core.parse_config()

    config.lint.fix = fix

    linter: core.Linter = core.Linter(config=config)

    core.BaseChecker.config = config

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    violations: core.ViolationMetric = core.ViolationMetric()

    files = core.filter_files(paths=paths, config=config)

    for source_path in source_paths:
        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:
            source_code: str = source_file.read()

        _violations: core.ViolationMetric = linter.run(
            file=pathlib.Path(file),
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
