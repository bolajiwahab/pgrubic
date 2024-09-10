"""Formatter."""

import sys
import pathlib

from pglast import ast, parser, stream, prettify, printers


@printers.node_printer(ast.CreateEnumStmt, override=True)  # type: ignore[misc]
def create_enum_stmt(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for CreateEnumStmt."""
    output.write("CREATE TYPE ")
    output.print_name(node.typeName)
    output.write("AS ENUM ")
    output.write("")
    with output.expression(need_parens=True):
        output.newline()
        output.space(4)
        output.print_list(node.vals, standalone_items=True)
        output.newline()


@printers.node_printer(ast.AlterEnumStmt, override=True)  # type: ignore[misc]
def alter_enum_stmt(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for AlterEnumStmt."""
    output.write("ALTER TYPE ")
    output.print_name(node.typeName)
    output.newline()
    output.space(4)
    if node.newVal:
        if node.oldVal:
            output.write("RENAME VALUE ")
            output.write_quoted_string(node.oldVal)
            output.write("TO ")
        else:
            output.write("ADD VALUE ")
            if node.skipIfNewValExists:
                output.write("IF NOT EXISTS ")
        output.write_quoted_string(node.newVal)
    if node.newValNeighbor:
        if node.newValIsAfter:
            output.write(" AFTER ")
        else:
            output.write(" BEFORE ")
        output.write_quoted_string(node.newValNeighbor)


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
