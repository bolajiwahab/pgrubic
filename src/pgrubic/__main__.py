"""Entry point."""

import os
import sys
import typing
import difflib
import logging
import pathlib
import multiprocessing
from collections import abc

import click
from rich.syntax import Syntax
from rich.console import Console

from pgrubic import PACKAGE_NAME, core
from pgrubic.core import noqa, errors

T = typing.TypeVar("T")

MAX_WORKERS_ENVIRONMENT_VARIABLE: typing.Final[str] = (
    f"{PACKAGE_NAME.upper()}_MAX_WORKERS"
)

DEFAULT_MAX_WORKERS: typing.Final[int] = 4

MAX_WORKERS: typing.Final[int] = int(
    os.getenv(MAX_WORKERS_ENVIRONMENT_VARIABLE, DEFAULT_MAX_WORKERS),
)


def common_options(func: abc.Callable[..., T]) -> abc.Callable[..., T]:
    """Decorator to add common options to each subcommand."""
    return click.option("--verbose", is_flag=True, help="Enable verbose logging.")(func)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog=f"""
Examples:\n
   {PACKAGE_NAME} lint\n
   {PACKAGE_NAME} lint .\n
   {PACKAGE_NAME} lint *.sql\n
   {PACKAGE_NAME} lint example.sql\n
   {PACKAGE_NAME} format file.sql\n
   {PACKAGE_NAME} format migrations/\n
""",
)
@click.version_option()
def cli() -> None:
    """Pgrubic: PostgreSQL linter and formatter for schema migrations
    and design best practices.
    """


@cli.command(name="lint")
@click.option(
    "--fix",
    is_flag=True,
    default=False,
    help="Fix lint violations automatically.",
)
@click.option(
    "--ignore-noqa",
    is_flag=True,
    default=False,
    help="Whether to ignore noqa directives.",
)
@click.option(
    "--add-file-level-general-noqa",
    is_flag=True,
    default=False,
    help="Whether to add file-level noqa directives.",
)
@common_options
@click.argument("sources", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def lint(  # noqa: C901, PLR0912
    sources: tuple[pathlib.Path, ...],
    *,
    verbose: bool,
    fix: bool,
    ignore_noqa: bool,
    add_file_level_general_noqa: bool,
) -> None:
    """Lint SQL files."""
    core.logger.setLevel(logging.INFO if verbose else logging.WARNING)

    config: core.Config = core.parse_config()

    for key, value in [("fix", fix), ("ignore_noqa", ignore_noqa)]:
        if value:
            setattr(config.lint, key, value)

    linter: core.Linter = core.Linter(config=config, formatters=core.load_formatters)

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    total_violations = 0
    auto_fixable_violations = 0
    fix_enabled_violations = 0

    # Use the current working directory if no sources are specified
    if not sources:
        sources = (pathlib.Path.cwd(),)

    included_sources: set[pathlib.Path] = core.filter_sources(
        sources=sources,
        include=config.lint.include,
        exclude=config.lint.exclude,
    )

    if add_file_level_general_noqa:
        sources_modified = noqa.add_file_level_general_ignore(included_sources)
        sys.stdout.write(
            f"File-level general noqa directive added to {sources_modified} file(s)\n",
        )

    # we set the number of processes to the least of available CPUs or the set MAX_WORKERS
    with multiprocessing.Pool(
        processes=min(multiprocessing.cpu_count(), MAX_WORKERS),
    ) as pool:
        try:
            results = [
                pool.apply_async(
                    linter.run,
                    kwds={
                        "source_file": source.resolve(),
                        "source_code": source.read_text(encoding="utf-8"),
                    },
                )
                for source in included_sources
            ]
            pool.close()
            pool.join()

            lint_results = [result.get() for result in results]

        except (errors.ParseError, errors.MissingStatementTerminatorError) as error:
            core.logger.error(error)
            sys.exit(2)

    for lint_result in lint_results:
        violations = linter.get_violation_stats(
            lint_result.violations,
        )

        linter.print_violations(
            violations=lint_result.violations,
            source_file=lint_result.source_file,
        )

        total_violations += violations.total
        auto_fixable_violations += violations.auto_fixable
        fix_enabled_violations += violations.fix_enabled

        if lint_result.fixed_sql:
            with pathlib.Path(lint_result.source_file).open(
                "w",
                encoding="utf-8",
            ) as sf:
                sf.write(lint_result.fixed_sql)

    if total_violations > 0:
        if config.lint.fix:
            sys.stdout.write(
                f"Found {total_violations} violation(s)"
                f" ({fix_enabled_violations} fixed,"
                f" {total_violations - fix_enabled_violations} remaining)\n",
            )

            if (total_violations - fix_enabled_violations) > 0:
                sys.exit(1)

        else:
            sys.stdout.write(
                f"Found {total_violations} violation(s)\n"
                f"{auto_fixable_violations} fix(es) available, {fix_enabled_violations} fix(es) enabled\n",  # noqa: E501
            )

            if auto_fixable_violations > 0:
                sys.stdout.write(
                    "Use with '--fix' to auto fix the violations\n",
                )

            sys.exit(1)


@cli.command(name="format")
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Check if any files would have been modified.",
)
@click.option(
    "--diff",
    is_flag=True,
    default=False,
    help="""
    Report the difference between the current file and
    how the formatted file would look like.""",
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Whether to read the cache.",
)
@common_options
@click.argument("sources", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))  # type: ignore [type-var]
def format_sql_file(  # noqa: C901
    sources: tuple[pathlib.Path, ...],
    *,
    check: bool,
    diff: bool,
    no_cache: bool,
    verbose: bool,
) -> None:
    """Format SQL files."""
    core.logger.setLevel(logging.INFO if verbose else logging.WARNING)

    console = Console()

    config: core.Config = core.parse_config()

    for key, value in [("check", check), ("diff", diff), ("no_cache", no_cache)]:
        if value:
            setattr(config.format, key, value)

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

    sources_to_reformat = included_sources

    if not config.format.no_cache:
        sources_to_reformat = cache.filter_sources(
            sources=included_sources,
        )

    changes_detected = False

    # we set the number of processes to the least of available CPUs or the set MAX_WORKERS
    with multiprocessing.Pool(
        processes=min(multiprocessing.cpu_count(), MAX_WORKERS),
    ) as pool:
        try:
            results = [
                pool.apply_async(
                    formatter.format,
                    kwds={
                        "source_file": source.resolve(),
                        "source_code": source.read_text(encoding="utf-8"),
                    },
                )
                for source in included_sources
            ]
            pool.close()
            pool.join()

            formatting_results = [result.get() for result in results]

        except (errors.ParseError, errors.MissingStatementTerminatorError) as error:
            core.logger.error(error)
            sys.exit(2)

    for formatting_result in formatting_results:
        if (
            formatting_result.formatted_source_code
            != formatting_result.original_source_code
            and not changes_detected
        ):
            changes_detected = True

        if config.format.diff:
            diff_unified = difflib.unified_diff(
                formatting_result.original_source_code.splitlines(keepends=True),
                formatting_result.formatted_source_code.splitlines(keepends=True),
                fromfile=str(formatting_result.source_file),
                tofile=str(formatting_result.source_file),
            )

            diff_output = "".join(diff_unified)
            console.print(Syntax(diff_output, "diff", theme="ansi_dark"))

        if not config.format.check and not config.format.diff:
            with pathlib.Path(formatting_result.source_file).open(
                "w",
                encoding="utf-8",
            ) as sf:
                sf.write(formatting_result.formatted_source_code)

    if not config.format.check and not config.format.diff:
        cache.write(sources=included_sources)
        sys.stdout.write(
            f"{len(sources_to_reformat)} file(s) reformatted, "
            f"{len(included_sources) - len(sources_to_reformat)} file(s) left unchanged\n",  # noqa: E501
        )

    if changes_detected and (config.format.check or config.format.diff):
        sys.exit(1)


if __name__ == "__main__":
    cli()
