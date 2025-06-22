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

from pgrubic import PACKAGE_NAME, DEFAULT_WORKERS, WORKERS_ENVIRONMENT_VARIABLE, core
from pgrubic.core import noqa, errors

T = typing.TypeVar("T")


def common_options(func: abc.Callable[..., T]) -> abc.Callable[..., T]:
    """Decorator to add common options to each subcommand."""
    func = click.version_option()(func)
    func = click.option("--workers", type=int, help="Number of workers to use.")(func)
    return click.option("--verbose", is_flag=True, help="Enable verbose logging.")(func)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog=f"""
Examples:{noqa.NEW_LINE}
   {PACKAGE_NAME} lint{noqa.NEW_LINE}
   {PACKAGE_NAME} lint .{noqa.NEW_LINE}
   {PACKAGE_NAME} lint *.sql{noqa.NEW_LINE}
   {PACKAGE_NAME} lint example.sql{noqa.NEW_LINE}
   {PACKAGE_NAME} format file.sql{noqa.NEW_LINE}
   {PACKAGE_NAME} format migrations/{noqa.NEW_LINE}
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
def lint(  # noqa: C901, PLR0912, PLR0913
    sources: tuple[pathlib.Path, ...],
    *,
    fix: bool,
    ignore_noqa: bool,
    add_file_level_general_noqa: bool,
    workers: int,
    verbose: bool,
) -> None:
    """Lint SQL files.

    Parameters:
    ----------
    sources: tuple[pathlib.Path, ...]
        List of sources to lint.
    fix: bool
        Fix lint violations automatically.
    ignore_noqa: bool
        Whether to ignore noqa directives.
    add_file_level_general_noqa: bool
        Whether to add file-level noqa directives.
    workers: int
        Number of workers to use.
    verbose: bool
        Enable verbose logging.

    Returns:
    -------
    None

    """
    core.logger.setLevel(logging.INFO if verbose else logging.WARNING)

    config: core.Config = core.parse_config()

    for key, value in [("fix", fix), ("ignore_noqa", ignore_noqa)]:
        if value:
            setattr(config.lint, key, value)

    linter: core.Linter = core.Linter(config=config, formatters=core.load_formatters)

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    # Use the current working directory if no sources are specified
    if not sources:
        sources = (pathlib.Path.cwd(),)

    included_sources: set[pathlib.Path] = core.filter_sources(
        sources=sources,
        include=config.lint.include,
        exclude=config.lint.exclude,
        respect_gitignore=config.respect_gitignore,
    )

    if add_file_level_general_noqa:
        sources_modified = noqa.add_file_level_general_lint_ignore(included_sources)
        sys.stdout.write(
            f"File-level general noqa directive added to {sources_modified} file(s){noqa.NEW_LINE}",  # noqa: E501
        )
        sys.exit(0)

    # the `--workers` flag when provided, takes precedence over the environment variable
    # the environment variable when provided, takes precedence over the default
    workers = (
        workers
        if workers
        else int(os.getenv(WORKERS_ENVIRONMENT_VARIABLE, DEFAULT_WORKERS))
    )

    # we set the number of processes to the smallest of these values:
    # 1. the number of CPUs
    # 2. the number of workers
    with multiprocessing.Pool(
        processes=min(
            multiprocessing.cpu_count(),
            workers,
        ),
    ) as pool:
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

    total_violations = 0
    auto_fixable_violations = 0
    fix_enabled_violations = 0
    total_errors = 0

    for lint_result in lint_results:
        violations = linter.get_violation_stats(
            lint_result.violations,
        )

        linter.print_violations(
            violations=lint_result.violations,
            source_file=lint_result.source_file,
        )

        errors.print_errors(
            errors=lint_result.errors,
            source_file=lint_result.source_file,
        )

        total_violations += violations.total
        auto_fixable_violations += violations.auto_fixable
        fix_enabled_violations += violations.fix_enabled
        total_errors += len(lint_result.errors)

        if lint_result.fixed_source_code:
            with pathlib.Path(lint_result.source_file).open(
                "w",
                encoding="utf-8",
            ) as sf:
                sf.write(lint_result.fixed_source_code)

    if total_violations > 0 or total_errors > 0:
        if config.lint.fix:
            sys.stdout.write(
                f"{noqa.NEW_LINE}Found {total_violations} violation(s)"
                f"{noqa.SPACE}({fix_enabled_violations} fixed,"
                f"{noqa.SPACE}{total_violations - fix_enabled_violations} remaining){noqa.NEW_LINE}"  # noqa: E501
                f"{total_errors} error(s) found{noqa.NEW_LINE}",
            )

            if (total_violations - fix_enabled_violations) > 0 or total_errors > 0:
                sys.exit(1)

        else:
            sys.stdout.write(
                f"{noqa.NEW_LINE}Found {total_violations} violation(s){noqa.NEW_LINE}"
                f"{auto_fixable_violations} fix(es) available, {fix_enabled_violations} fix(es) enabled{noqa.NEW_LINE}"  # noqa: E501
                f"{total_errors} error(s) found{noqa.NEW_LINE}",
            )

            if auto_fixable_violations > 0:
                sys.stdout.write(
                    f"Use with '--fix' to auto fix the violations{noqa.NEW_LINE}",
                )

            sys.exit(1)
    else:
        sys.stdout.write(f"All checks passed!{noqa.NEW_LINE}")


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
def format_sources(  # noqa: C901, PLR0912, PLR0913
    sources: tuple[pathlib.Path, ...],
    *,
    check: bool,
    diff: bool,
    no_cache: bool,
    workers: int,
    verbose: bool,
) -> None:
    """Format SQL files.

    Parameters:
    ----------
    sources: tuple[pathlib.Path, ...]
        List of sources to format.
    check: bool
        Check if any files would have been modified.
    diff: bool
        Report the difference between the current file and
        how the formatted file would look like.
    no_cache: bool
        Whether to read the cache.
    workers: int
        Number of workers to use.
    verbose: bool
        Enable verbose logging.

    Returns:
    -------
    None

    """
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
        respect_gitignore=config.respect_gitignore,
    )

    cache = core.Cache(config=config)

    sources_to_format = included_sources

    if not config.format.no_cache:
        sources_to_format = cache.filter_sources(
            sources=included_sources,
        )

    # the `--workers` flag when specified, takes precedence over the environment variable
    # the environment variable when provided, takes precedence over the default
    workers = (
        workers
        if workers
        else int(os.getenv(WORKERS_ENVIRONMENT_VARIABLE, DEFAULT_WORKERS))
    )

    # we set the number of processes to the smallest of these values:
    # 1. the number of CPUs
    # 2. the number of workers
    with multiprocessing.Pool(
        processes=min(
            multiprocessing.cpu_count(),
            workers,
        ),
    ) as pool:
        results = [
            pool.apply_async(
                formatter.format,
                kwds={
                    "source_file": source.resolve(),
                    "source_code": source.read_text(encoding="utf-8"),
                },
            )
            for source in sources_to_format
        ]
        pool.close()
        pool.join()

        formatting_results = [result.get() for result in results]

    changes_detected = False
    total_errors = 0

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

            if diff_output:
                console.print(Syntax(diff_output, "diff", theme="ansi_dark"))

        if not config.format.check and not config.format.diff:
            with pathlib.Path(formatting_result.source_file).open(
                "w",
                encoding="utf-8",
            ) as sf:
                sf.write(formatting_result.formatted_source_code)

        errors.print_errors(
            errors=formatting_result.errors,
            source_file=formatting_result.source_file,
        )

        total_errors += len(formatting_result.errors)

    if not config.format.check and not config.format.diff:
        cache.write(sources=sources_to_format)
        sys.stdout.write(
            f"{noqa.NEW_LINE}{len(sources_to_format)} file(s) reformatted, "
            f"{len(included_sources) - len(sources_to_format)} file(s) left unchanged{noqa.NEW_LINE}",  # noqa: E501
        )
        if total_errors > 0:
            sys.stdout.write(f"{total_errors} error(s) found{noqa.NEW_LINE}")
            sys.exit(1)

        sys.exit(0)

    if (
        changes_detected and (config.format.check or config.format.diff)
    ) or total_errors > 0:
        if total_errors > 0:
            sys.stdout.write(
                f"{noqa.NEW_LINE}{total_errors} error(s) found{noqa.NEW_LINE}",
            )
        sys.exit(1)


if __name__ == "__main__":
    cli()
