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

from pgrubic import PACKAGE_NAME, core

T = typing.TypeVar("T")


def common_options(func: abc.Callable[..., T]) -> abc.Callable[..., T]:
    """Decorator to add common options to each subcommand."""
    return click.option("--verbose", is_flag=True, help="Enable verbose logging.")(func)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog=f"""
Examples:\n
   {PACKAGE_NAME} lint .\n
   {PACKAGE_NAME} lint *.sql\n
   {PACKAGE_NAME} lint example.sql\n
   {PACKAGE_NAME} format src/queries\n
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
@click.argument("sources", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def lint(
    sources: tuple[pathlib.Path, ...],
    *,
    verbose: bool,
    fix: bool,
    ignore_noqa: bool,
) -> None:
    """Lint SQL files."""
    core.logger.setLevel(logging.INFO if verbose else logging.WARNING)

    config: core.Config = core.parse_config()

    if fix:
        config.lint.fix = fix

    if ignore_noqa:
        config.lint.ignore_noqa = ignore_noqa

    linter: core.Linter = core.Linter(config=config, formatters=core.load_formatters)

    core.BaseChecker.config = config

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    total_violations = 0
    fixable_violations = 0

    # Use the current working directory if no sources are specified
    if not sources:
        sources = (pathlib.Path.cwd(),)

    included_sources: set[pathlib.Path] = core.filter_sources(
        sources=sources,
        include=config.lint.include,
        exclude=config.lint.exclude,
    )

    for source in included_sources:
        source_file = source.resolve()
        source_code = source.read_text(encoding="utf-8")

        lint_result = linter.run(
            source_file=str(source_file),
            source_code=source_code,
        )

        violations = linter.get_violation_stats(
            lint_result.violations,
        )

        linter.print_violations(
            violations=lint_result.violations,
            source_file=str(source_file),
        )

        total_violations += violations.total
        fixable_violations += violations.fixable

        if lint_result.fixed_sql:
            with source_file.open("w", encoding="utf-8") as sf:
                sf.write(lint_result.fixed_sql)

    # if total_violations > 0:
    if config.lint.fix:
        sys.stdout.write(
            f"Found {total_violations} violation(s)"
            f" ({fixable_violations} fixed,"
            f" {total_violations - fixable_violations} remaining)\n",
        )

        if (total_violations - fixable_violations) > 0:
            sys.exit(1)

    else:
        sys.stdout.write(
            f"Found {total_violations} violation(s)\n"
            f"{fixable_violations} fix(es) available\n",
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
@click.argument("sources", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def format_sql_file(
    sources: tuple[pathlib.Path, ...],
    *,
    check: bool,
    diff: bool,
    verbose: bool,
) -> None:
    """Format SQL files."""
    core.logger.setLevel(logging.INFO if verbose else logging.WARNING)

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

    # Use the current working directory if no sources are specified
    if not sources:
        sources = (pathlib.Path.cwd(),)

    included_sources = core.filter_sources(
        sources=sources,
        include=config.format.include,
        exclude=config.format.exclude,
    )

    cache = core.Cache(config=config)

    sources_to_be_formatted = cache.filter_sources(
        sources=typing.cast(tuple[pathlib.Path, ...], included_sources),
    )

    formatted_sources: int = 0

    for source in sources_to_be_formatted:
        source_file = source.resolve()
        source_code = source.read_text(encoding="utf-8")

        formatted_source_code = formatter.format(
            source_file=str(source_file),
            source_code=source_code,
        )

        if formatted_source_code != source_code:
            formatted_sources += 1

        if config.format.diff:
            diff_unified = difflib.unified_diff(
                source_code.splitlines(keepends=True),
                formatted_source_code.splitlines(keepends=True),
                fromfile=str(source_file),
                tofile=str(source_file),
            )

            diff_output = "".join(diff_unified)
            console.print(Syntax(diff_output, "diff", theme="ansi_dark"))

        if (
            formatted_source_code != source_code
            and not config.format.check
            and not config.format.diff
        ):
            with source_file.open("w", encoding="utf-8") as sf:
                sf.write(formatted_source_code)

    if not config.format.check and not config.format.diff:
        cache.write(sources=typing.cast(tuple[pathlib.Path, ...], included_sources))
        sys.stdout.write(
            f"{formatted_sources} file(s) reformatted\n",
        )

    if formatted_sources != 0 and (config.format.check or config.format.diff):
        sys.exit(1)


if __name__ == "__main__":
    cli()
