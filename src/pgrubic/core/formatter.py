"""Formatter."""

import sys
import pathlib

from pglast import parser, prettify


class Formatter:
    """Format source file."""

    @staticmethod
    def _run(*, source_path: str, comma_at_eoln: bool) -> str:
        """Format source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:
            source_code = source_file.read()

        try:
            parser.parse_sql(source_code)

        except parser.ParseError as error:
            sys.stdout.write(f"{file_name}: {error!s}")

            sys.exit(1)

        return str(
            prettify(
                statement=source_code,
                preserve_comments=True,
                comma_at_eoln=comma_at_eoln,
            ),
        )

    def diff(self, *, source_path: str, comma_at_eoln: bool = True) -> None:
        """Print all diffs collected by the formatter."""
        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:
            source_code = source_file.read()

        result = self._run(source_path=source_path, comma_at_eoln=comma_at_eoln)

        if source_code != result:
            sys.stdout.write(result)

    def format(self, *, source_path: str, comma_at_eoln: bool = True) -> None:
        """Format source file."""
        result = self._run(source_path=source_path, comma_at_eoln=comma_at_eoln)

        with pathlib.Path(source_path).open("w", encoding="utf-8") as source_file:
            source_file.write(result)
