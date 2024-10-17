"""Formatter."""

import sys
import typing
import difflib
import pathlib

from pglast import ast, parser, stream
from colorama import Fore, Style

from pgrubic.core import noqa, config


class FormatResult(typing.NamedTuple):
    """Representation of the result of formatting."""

    exit_code: int
    output: str


class Formatter:
    """Format source file."""

    def __init__(self, config: config.Config) -> None:
        """Initialize variables."""
        self.config = config

    @staticmethod
    def run(*, source_file: str, source_code: str, config: config.Config) -> str:
        """Format source file."""
        try:
            tree: ast.Node = parser.parse_sql(source_code)
            comments = noqa.extract_comments(source_code)

        except parser.ParseError as error:
            sys.stderr.write(f"{source_file}: {Fore.RED}{error!s}{Style.RESET_ALL}")

            sys.exit(1)

        return (
            str(
                stream.IndentedStream(
                    comments=comments,
                    semicolon_after_last_statement=config.format.semicolon_after_last_statement,
                    separate_statements=config.format.separate_statements,
                    remove_pg_catalog_from_functions=config.format.remove_pg_catalog_from_functions,
                    comma_at_eoln=config.format.comma_at_eoln,
                )(tree),
            )
            + "\n"
        )

    def format(self, *, source_file: str, source_code: str) -> FormatResult:
        """Format source code."""
        source_file = pathlib.Path(source_file).name

        formatted_source_code = self.run(
            source_file=source_file,
            source_code=source_code,
            config=self.config,
        )

        if self.config.format.check and formatted_source_code != source_code:
            return FormatResult(exit_code=1, output="")

        if self.config.format.diff and formatted_source_code != source_code:
            diff = difflib.unified_diff(
                source_code.splitlines(keepends=True),
                formatted_source_code.splitlines(keepends=True),
                fromfile=source_file,
                tofile=source_file,
            )
            diff_output = "".join(diff)

            return FormatResult(exit_code=1, output=diff_output)

        return FormatResult(exit_code=0, output=formatted_source_code)
