"""Formatter."""

import sys
import difflib
import pathlib

from pglast import parser, prettify
from rich.syntax import Syntax
from rich.console import Console

from pgrubic.core import config


class Formatter:
    """Format source file."""

    def __init__(self, config: config.Config) -> None:
        """Initialize variables."""
        self.config = config

    @staticmethod
    def run(*, source_file: str, source_code: str, config: config.Config) -> str:
        """Format source file."""
        try:
            parser.parse_sql(source_code)

        except parser.ParseError as error:
            sys.stdout.write(f"{source_file}: {error!s}")

            sys.exit(1)

        return str(
            prettify(
                statement=source_code,
                preserve_comments=True,
                comma_at_eoln=config.format.comma_at_eoln,
            ),
        )

    def format(self, *, source_file: str, source_code: str) -> None:
        """Format source code."""
        source_file = pathlib.Path(source_file).name

        formatted_source_code = self.run(
            source_file=source_file,
            source_code=source_code,
            config=self.config,
        )

        if self.config.format.check and formatted_source_code != source_code:
            sys.exit(1)

        if self.config.format.diff and formatted_source_code != source_code:
            console = Console()
            diff = difflib.unified_diff(
                source_code.splitlines(keepends=True),
                formatted_source_code.splitlines(keepends=True),
                fromfile=source_file,
                tofile=source_file,
            )
            diff_output = "".join(diff)

            console.print(Syntax(diff_output, "diff", theme="ansi_dark"))
            sys.exit(1)

        with pathlib.Path(source_file).open("w", encoding="utf-8") as sf:
            sf.write(formatted_source_code)
