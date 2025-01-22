"""Formatter."""

import typing

from pglast import parser, stream

from pgrubic.core import noqa, config, errors


class FormatResult(typing.NamedTuple):
    """Format Result."""

    source_file: str
    original_source_code: str
    formatted_source_code: str


class Formatter:
    """Format source code."""

    def __init__(
        self,
        *,
        config: config.Config,
        formatters: typing.Callable[[], set[typing.Callable[[], None]]],
    ) -> None:
        """Initialize variables."""
        self.formatters = formatters()
        self.config = config

    @staticmethod
    def run(*, source_file: str, source_code: str, config: config.Config) -> str:
        """Format source code.

        Parameters:
        ----------
        source_file: str
            Path to the source file.
        source_code: str
            Source code to format.

        Returns:
        -------
        str
            Formatted source code.

        Raises:
        ------
        ParseError
            If there is an error parsing source code.
        """
        try:
            parser.parse_sql(source_code)

        except parser.ParseError as error:
            msg = "Error parsing source code: "
            raise errors.ParseError(f"{source_file}: " + msg + str(error)) from error

        formatted_statements: list[str] = []

        format_ignores = noqa.extract_format_ignores(
            source_file=source_file,
            source_code=source_code,
        )

        for statement in noqa.extract_statement_locations(
            source_file=source_file,
            source_code=source_code,
        ):
            if statement.start_location in format_ignores:
                formatted_statements.append(statement.text)
                continue

            comments = noqa.extract_comments(
                source_file=source_file,
                source_code=statement.text,
            )

            formatted_statement = stream.IndentedStream(
                comments=comments,
                semicolon_after_last_statement=False,
                remove_pg_catalog_from_functions=config.format.remove_pg_catalog_from_functions,
                comma_at_eoln=not (config.format.comma_at_beginning),
                special_functions=True,
            )(statement.text)

            if config.format.new_line_before_semicolon:
                formatted_statement += noqa.NEW_LINE + noqa.SEMI_COLON
            else:
                formatted_statement += noqa.SEMI_COLON

            formatted_statements.append(formatted_statement)

        return (
            noqa.NEW_LINE + (noqa.NEW_LINE * config.format.lines_between_statements)
        ).join(
            formatted_statements,
        ) + noqa.NEW_LINE

    def format(self, *, source_file: str, source_code: str) -> FormatResult:
        """Format source code.

        Parameters:
        ----------
        source_file: str
            Path to the source file.
        source_code: str
            Source code to format.

        Returns:
        -------
        FormatResult
            Formatted source code.
        """
        return FormatResult(
            source_file=source_file,
            original_source_code=source_code,
            formatted_source_code=self.run(
                source_file=source_file,
                source_code=source_code,
                config=self.config,
            ),
        )
