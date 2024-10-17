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

    # Use the current working directory if no paths are specified
    if not paths:
        paths = (pathlib.Path.cwd(),)

    source_files = core.filter_files(
        paths=paths,
        include=config.lint.include,
        exclude=config.lint.exclude,
    )

    for source_file in source_files:
        with source_file.open("r", encoding="utf-8") as sf:
            source_code: str = sf.read()

        _violations: core.ViolationMetric = linter.run(
            source_file=str(source_file),
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

            if violations.fixable_manual_total > 0:
                sys.exit(1)

        else:
            sys.stdout.write(
                f"Found {violations.total} violations.\n"
                f"{violations.fixable_auto_total} fixes available.\n",
            )

            sys.exit(1)


@cli.command(name="format")
@click.option(
    "--check",
    is_flag=True,
    help="Check if any files would have been modified",
)
@click.option(
    "--diff",
    is_flag=True,
    help="""
    Report the difference between the current file and
    how the formatted file would look like""",
)
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def format_sql_file(
    paths: tuple[pathlib.Path, ...],
    *,
    check: bool,
    diff: bool,
) -> None:
    """Format SQL files."""
    config: core.Config = core.parse_config()
    config.format.check = check
    config.format.diff = diff

    formatter: core.Formatter = core.Formatter(config=config)

    source_files = core.filter_files(
        paths=paths,
        include=config.format.include,
        exclude=config.format.exclude,
    )

    for source_file in source_files:
        with source_file.open("r", encoding="utf-8") as sf:
            source_code: str = sf.read()

        formatter.format(source_file=str(source_file), source_code=source_code)


if __name__ == "__main__":
    cli()
