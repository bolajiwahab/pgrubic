"""Formatter."""

import typing

from pglast import parser, stream

from pgrubic import ISSUES_URL
from pgrubic.core import noqa, config, errors


class FormatResult(typing.NamedTuple):
    """Format Result."""

    source_file: str
    original_source_code: str
    formatted_source_code: str
    errors: set[errors.Error]


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
    def run(
        *,
        source_file: str,
        source_code: str,
        config: config.Config,
    ) -> tuple[str, set[errors.Error]]:
        """Format source code.

        Parameters:
        ----------
        source_file: str
            Path to the source file.
        source_code: str
            Source code to format.

        Returns:
        -------
        tuple[str, set[errors.Error]]
            Formatted source code.
        """
        _errors: set[errors.Error] = set()

        formatted_statements: list[str] = []

        statements = noqa.extract_statements(
            source_code=source_code,
        )

        is_file_format_skip = noqa.check_file_format_skip(
            source_code=source_code,
        )

        if not is_file_format_skip:
            for statement in statements:
                if noqa.check_statement_format_skip(
                    source_code=source_code,
                    statement=statement,
                ):
                    formatted_statements.append(statement.text)
                    continue

                comments = noqa.extract_comments(
                    statement=statement,
                )

                try:
                    parser.parse_sql(statement.text)

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

                except parser.ParseError as error:
                    _errors.add(
                        errors.Error(
                            source_file=str(source_file),
                            source_code=statement.text,
                            statement_start_location=statement.start_location + 1,
                            statement_end_location=statement.end_location,
                            statement=statement.text,
                            message=str(error),
                            hint=f"""Make sure the statement is valid PostgreSQL statement. If it is, please report this issue at {ISSUES_URL}{noqa.NEW_LINE}""",  # noqa: E501
                        ),
                    )
                    formatted_statements.append(statement.text.strip(noqa.NEW_LINE))

                except RecursionError as error:  # pragma: no cover
                    _errors.add(
                        errors.Error(
                            source_file=str(source_file),
                            source_code=statement.text,
                            statement_start_location=statement.start_location + 1,
                            statement_end_location=statement.end_location,
                            statement=statement.text,
                            message=str(error),
                            hint="Maximum format depth exceeded, reduce deeply nested queries",  # noqa: E501
                        ),
                    )
                    formatted_statements.append(statement.text.strip(noqa.NEW_LINE))

            return (
                noqa.NEW_LINE + (noqa.NEW_LINE * config.format.lines_between_statements)
            ).join(
                formatted_statements,
            ) + noqa.NEW_LINE, _errors

        return source_code, _errors

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
        formatted_source_code, errors = self.run(
            source_file=source_file,
            source_code=source_code,
            config=self.config,
        )
        return FormatResult(
            source_file=source_file,
            original_source_code=source_code,
            formatted_source_code=formatted_source_code,
            errors=errors,
        )
