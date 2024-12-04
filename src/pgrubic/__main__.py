"""Entry point."""

import sys
import typing
import difflib
import logging
import pathlib
from collections import abc

import click
from rich.syntax import Syntax
from rich.console import Console

from pgrubic import PROGRAM_NAME, core
from pgrubic.core import noqa

T = typing.TypeVar("T")


def common_options(func: abc.Callable[..., T]) -> abc.Callable[..., T]:
    """Decorator to add common options to each subcommand."""
    return click.option("--verbose", is_flag=True, help="Enable verbose logging.")(func)


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
@click.option(
    "--fix",
    is_flag=True,
    default=None,
    help="Fix lint violations automatically.",
)
@click.option(
    "--ignore-noqa",
    is_flag=True,
    default=None,
    help="Whether to ignore noqa directives.",
)
@common_options
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def lint(
    paths: tuple[pathlib.Path, ...],
    *,
    verbose: bool,
    fix: bool,
    ignore_noqa: bool,
) -> None:
    """Lint SQL files."""
    if verbose:
        core.logger.setLevel(logging.INFO)

    config: core.Config = core.parse_config()

    if fix:
        config.lint.fix = fix

    if ignore_noqa:
        config.lint.ignore_noqa = ignore_noqa

    linter: core.Linter = core.Linter(config=config)

    core.BaseChecker.config = config

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    total_violations = 0
    fixable_violations = 0

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

        lint_result = linter.run(
            source_file=str(source_file),
            source_code=source_code,
        )

        violations = linter.get_violation_stats(
            lint_result.violations,
        )

        total_violations += violations.total
        fixable_violations += violations.fixable

    if total_violations > 0:
        if config.lint.fix is True:
            sys.stdout.write(
                f"Found {total_violations} violations"
                f" ({fixable_violations} fixed,"
                f" {total_violations - fixable_violations} remaining).\n",
            )

            if (total_violations - fixable_violations) > 0:
                sys.exit(1)

        else:
            sys.stdout.write(
                f"Found {total_violations} violations.\n"
                f"{fixable_violations} fixes available.\n",
            )

            sys.exit(1)


@cli.command(name="format")
@click.option(
    "--check",
    is_flag=True,
    default=None,
    help="Check if any files would have been modified.",
)
@click.option(
    "--diff",
    is_flag=True,
    default=None,
    help="""
    Report the difference between the current file and
    how the formatted file would look like.""",
)
@common_options
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def format_sql_file(
    paths: tuple[pathlib.Path, ...],
    *,
    check: bool,
    diff: bool,
    verbose: bool,
) -> None:
    """Format SQL files."""
    if verbose:
        core.logger.setLevel(logging.INFO)

    console = Console()
    config: core.Config = core.parse_config()

    if check:
        config.format.check = check

    if diff:
        config.format.diff = diff

    formatter: core.Formatter = core.Formatter(
        config=config,
        formatters=core.load_formatters,
    )

    # Use the current working directory if no paths are specified
    if not paths:
        paths = (pathlib.Path.cwd(),)

    source_files = core.filter_files(
        paths=paths,
        include=config.format.include,
        exclude=config.format.exclude,
    )

    files_requiring_formatting: list[pathlib.Path] = []

    for source_file in source_files:
        with source_file.open("r", encoding="utf-8") as sf:
            source_code: str = sf.read()
            source_code = (
                source_code
                if source_code.endswith(noqa.NEW_LINE)
                else source_code + noqa.NEW_LINE
            )

        formatted_source_code = formatter.format(
            source_file=str(source_file),
            source_code=source_code,
        )

        if formatted_source_code != source_code and config.format.check:
            files_requiring_formatting.append(source_file)

        if formatted_source_code != source_code and config.format.diff:
            diff_unified = difflib.unified_diff(
                source_code.splitlines(keepends=True),
                formatted_source_code.splitlines(keepends=True),
                fromfile=str(source_file),
                tofile=str(source_file),
            )

            diff_output = "".join(diff_unified)
            console.print(Syntax(diff_output, "diff", theme="ansi_dark"))

            files_requiring_formatting.append(source_file)

        if (
            formatted_source_code != source_code
            and not config.format.check
            and not config.format.diff
        ):
            with source_file.open("w", encoding="utf-8") as sf:
                sf.write(formatted_source_code)

    if len(files_requiring_formatting) > 0:
        sys.exit(1)


if __name__ == "__main__":
    cli()
