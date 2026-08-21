"""CLI help presentation."""

import inspect
from collections import abc

import click

from pgrubic import PACKAGE_NAME

CONFIG_OVERRIDE_HELP = """A TOML `<KEY> = <VALUE>` pair overriding a configuration option.
May be repeated. Command-line overrides always take precedence over configuration
files.

\b
Examples:
  --config "lint.target-postgres-version = 17"
  --config 'format.type-casting-style = "native"'
"""

ROOT_EPILOG = f"""\b
{click.style("Configuration overrides:", fg="cyan", bold=True)}
  Pass a TOML `<KEY> = <VALUE>` pair. May be repeated.
    --config "lint.target-postgres-version = 17"
    --config 'format.type-casting-style = "native"'

\b
{click.style("Examples:", fg="cyan", bold=True)}
  {PACKAGE_NAME} lint .
  {PACKAGE_NAME} lint --fix migrations/
  {PACKAGE_NAME} format schema.sql
  {PACKAGE_NAME} format --check migrations/
"""


class HelpFormatter(click.HelpFormatter):
    """Render CLI help with terminal-aware colors."""

    def write_usage(
        self,
        prog: str,
        args: str = "",
        prefix: str | None = None,
    ) -> None:
        """Write a usage line with a colored heading and command."""
        if prefix is None:
            prefix = f"{click.style('Usage:', fg='cyan', bold=True)} "
        super().write_usage(
            click.style(prog, fg="green", bold=True),
            click.style(args, fg="green", bold=True),
            prefix,
        )

    def write_heading(self, heading: str) -> None:
        """Write a colored section heading."""
        super().write_heading(click.style(heading, fg="cyan", bold=True))

    def write_dl(
        self,
        rows: abc.Iterable[abc.Iterable[str]],
        col_max: int = 30,
        col_spacing: int = 2,
    ) -> None:
        """Write a definition list with colored options and commands."""
        super().write_dl(
            ((click.style(term, fg="green"), description) for term, description in rows),
            col_max,
            col_spacing,
        )


class Context(click.Context):
    """Click context using pgrubic's help formatter."""

    formatter_class = HelpFormatter


def _format_help(
    command: click.Command,
    ctx: click.Context,
    formatter: click.HelpFormatter,
) -> None:
    """Write help with a flush-left description before usage."""
    description = inspect.cleandoc(command.help or "").partition("\f")[0]
    if description:
        formatter.write_text(description)
        formatter.write_paragraph()

    command.format_usage(ctx, formatter)
    command.format_options(ctx, formatter)
    command.format_epilog(ctx, formatter)


class Command(click.Command):
    """Click command using pgrubic's context."""

    context_class = Context

    def format_help(
        self,
        ctx: click.Context,
        formatter: click.HelpFormatter,
    ) -> None:
        """Write help with the description before usage, as Ruff does."""
        _format_help(self, ctx, formatter)


class Group(click.Group):
    """Click group whose subcommands use pgrubic's help formatting."""

    context_class = Context
    command_class = Command

    def format_help(
        self,
        ctx: click.Context,
        formatter: click.HelpFormatter,
    ) -> None:
        """Write help with the description before usage, as Ruff does."""
        _format_help(self, ctx, formatter)

    def format_options(
        self,
        ctx: click.Context,
        formatter: click.HelpFormatter,
    ) -> None:
        """Write commands before root options."""
        self.format_commands(ctx, formatter)
        click.Command.format_options(self, ctx, formatter)

    def format_epilog(
        self,
        ctx: click.Context,
        formatter: click.HelpFormatter,
    ) -> None:
        """Write root help examples without indenting their headings."""
        if self.epilog:
            formatter.write_paragraph()
            formatter.write_text(inspect.cleandoc(self.epilog))
