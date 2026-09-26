"""Formatter."""

import typing

from pglast import Comment, ast, parser, stream

from pgrubic import ISSUES_URL
from pgrubic.core import noqa, config, errors
from pgrubic.postgres import functions as postgres_functions


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
        """Extend RawStream with config and source code."""
        self.config = config
        self.source_code = source_code

        super().__init__(**options)

    def write_empty_string(self) -> None:
        """Write an empty string (no-op)."""
        self.write("")

    def write_as_keyword(self, text: str) -> None:
        """Write text as a keyword using the configured keyword casing."""
        self.write(
            text.upper() if self.config.format.uppercase_keywords else text.lower(),
        )

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
        """Initialize IndentedStream with config and source code."""
        self.config = config
        self.source_code = source_code

        super().__init__(**options)

    def print_comment(self, comment: Comment) -> None:
        """Print comments on their own line."""
        self.write(comment.text)
        self.newline()

    @staticmethod
    def lowercase_keywords(*, text: str) -> str:
        """Lowercase keywords in the given text.

        Parameters:
        ----------
        text: str
            Text containing keywords to lowercase.

        Returns:
        -------
        str
            Text with lowercase keywords.
        """
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

    def write_as_keyword(self, text: str) -> None:
        """Write text as a keyword using the configured keyword casing."""
        self.write(
            text.upper() if self.config.format.uppercase_keywords else text.lower(),
        )

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
                    parse_tree = parser.parse_sql(statement.text)
                    parsed_statement = parse_tree[0].stmt

                    if isinstance(
                        parsed_statement,
                        (ast.CreateFunctionStmt, ast.DoStmt),
                    ) and not postgres_functions.has_body(parsed_statement):
                        _errors.add(
                            errors.Error(
                                source_file=str(source_file),
                                source_code=statement.text,
                                statement_start_location=statement.start_location + 1,
                                statement_end_location=statement.end_location,
                                statement=statement.text,
                                message="No routine body specified",
                                hint="Specify the routine body using AS or a SQL body",
                            ),
                        )
                        formatted_statements.append(
                            statement.text.strip(noqa.NEW_LINE),
                        )
                        continue

                    formatted_statement = Formatter._render_ast(
                        source_ast=parse_tree,
                        source_code=statement.text,
                        comments=comments,
                        config=config,
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
        return self._render_ast(
            source_ast=source_ast,
            source_code=source_code,
            comments=comments,
            config=self.config,
        )

    @staticmethod
    def _render_ast(
        *,
        source_ast: tuple[ast.RawStmt, ...],
        source_code: str | None,
        comments: list[Comment],
        config: config.Config,
    ) -> str:
        """Render source code from AST."""
        output = IndentedStream(
            config=config,
            source_code=source_code,
            comments=comments,
            semicolon_after_last_statement=False,
            separate_statements=config.format.lines_between_statements,
            remove_pg_catalog_from_functions=(
                config.format.remove_pg_catalog_from_functions
            ),
            comma_at_eoln=not config.format.comma_at_beginning,
            special_functions=(config.format.rewrite_function_calls_as_equivalent_syntax),
        )

        formatted_source = output(source_ast)

        if config.format.uppercase_keywords:
            return formatted_source

        return IndentedStream.lowercase_keywords(text=formatted_source)
