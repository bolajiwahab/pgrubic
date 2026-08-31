"""Formatter."""

import typing

from pglast import Comment, ast, parser, stream

from pgrubic import ISSUES_URL
from pgrubic.core import noqa, config, errors


class FormatResult(typing.NamedTuple):
    """Format Result."""

    source_file: str
    original_source_code: str
    formatted_source_code: str
    errors: set[errors.Error]


class RawStream(stream.RawStream):
    """Raw SQL parse tree writer."""

    def __init__(
        self,
        config: config.Config,
        source_code: str | None = None,
        **options: typing.Any,
    ) -> None:
        """Extend RawStream with config."""
        super().__init__(**options)
        self.config = config
        self.source_code = source_code

    def write_empty_string(self) -> None:
        """Write an empty string (no-op)."""
        self.write("")

    def print_parenthesized_list(
        self,
        nodes: tuple[ast.Node, ...],
        *,
        closing_indent: int,
        continuation_indent: int = 4,
    ) -> None:
        """Print a compact parenthesized list."""
        # RawStream suppresses pending separators before "(", so force the
        # caller-requested space to match pglast's DDL serialization.
        self.space(force=True)
        with self.expression(need_parens=True):
            self.print_list(nodes, standalone_items=False)


class IndentedStream(stream.IndentedStream):
    """Indented SQL parse tree writer."""

    def __init__(
        self,
        config: config.Config,
        source_code: str | None = None,
        **options: typing.Any,
    ) -> None:
        """Initialize IndentedStream with config."""
        super().__init__(**options)
        self.config = config
        self.source_code = source_code

    def apply_keyword_case(self, *, text: str) -> str:
        """Apply the configured casing to keywords in the given text.

        Parameters:
        ----------
        text: str
            Text to apply keyword casing to.

        Returns:
        -------
        str
            Formatted output with keyword casing applied.
        """
        if self.config.format.uppercase_keywords:
            return text

        output = list(text)
        for token in parser.scan(text):
            if token.kind != "NO_KEYWORD":
                output[token.start : token.end + 1] = text[
                    token.start : token.end + 1
                ].lower()

        return "".join(output)

    def _concatenate_nodes(
        self,
        *,
        nodes: tuple[ast.Node, ...],
        sep: str = noqa.SPACE,
        are_names: bool = False,
    ) -> str:
        """Concatenate the given `nodes`, using `sep` as the separator."""
        output = RawStream(
            config=self.config,
            source_code=self.source_code,
            special_functions=self.special_functions,
            remove_pg_catalog_from_functions=self.remove_pg_catalog_from_functions,
        )

        output.print_list(
            nodes=nodes,
            sep=sep,
            standalone_items=False,
            are_names=are_names,
        )

        return output.getvalue()

    def write_empty_string(self) -> None:
        """Write an empty string (no-op)."""
        self.write("")

    def print_parenthesized_list(
        self,
        nodes: tuple[ast.Node, ...],
        *,
        closing_indent: int,
        continuation_indent: int = 4,
    ) -> None:
        """Print a parenthesized list in compact or expanded form."""
        compact_list = self._concatenate_nodes(nodes=nodes)
        compact_parenthesized_lists_margin = (
            self.config.format.compact_parenthesized_lists_margin
        )
        length_of_parentheses = 2
        is_compact = compact_parenthesized_lists_margin > 0 and (
            (self.current_column + len(compact_list) + length_of_parentheses)
            <= compact_parenthesized_lists_margin
        )

        self.write("(")
        if is_compact:
            self.print_list(nodes, standalone_items=False)
        else:
            self.newline()
            self.space(continuation_indent)
            self.print_list(nodes, standalone_items=True)
            self.newline()
            self.indent(closing_indent)
        self.write(")")
        if not is_compact:
            self.dedent()


type PrinterOutput = RawStream | IndentedStream


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

    def create_raw_stream(self) -> RawStream:
        """Create a raw stream with the formatter's configuration."""
        return RawStream(
            config=self.config,
            special_functions=(
                self.config.format.rewrite_function_calls_as_equivalent_syntax
            ),
            remove_pg_catalog_from_functions=(
                self.config.format.remove_pg_catalog_from_functions
            ),
        )

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

                    output = IndentedStream(
                        config=config,
                        source_code=statement.text,
                        comments=comments,
                        semicolon_after_last_statement=False,
                        remove_pg_catalog_from_functions=config.format.remove_pg_catalog_from_functions,
                        comma_at_eoln=not (config.format.comma_at_beginning),
                        special_functions=config.format.rewrite_function_calls_as_equivalent_syntax,
                    )
                    formatted_statement = output.apply_keyword_case(
                        text=output(statement.text),
                    )

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

    def format_ast(
        self,
        *,
        source_ast: tuple[ast.RawStmt, ...],
        source_code: str | None = None,
        comments: list[Comment],
    ) -> str:
        """Format source code from AST.

        Parameters:
        ----------
        source_ast: tuple[ast.RawStmt, ...]
            Source AST to format.
        source_code: str | None
            Original source code associated with the AST.
        comments: list[noqa.Comment]
            Comments extracted from the original statement.

        Returns:
        -------
        str
            Formatted source code.
        """
        output = IndentedStream(
            config=self.config,
            source_code=source_code,
            comments=comments,
            semicolon_after_last_statement=False,
            separate_statements=self.config.format.lines_between_statements,
            remove_pg_catalog_from_functions=self.config.format.remove_pg_catalog_from_functions,
            comma_at_eoln=not (self.config.format.comma_at_beginning),
            special_functions=self.config.format.rewrite_function_calls_as_equivalent_syntax,
        )
        return output.apply_keyword_case(text=output(source_ast))
