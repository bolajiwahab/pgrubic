"""Formatter."""

import sys
import pathlib

from pglast import ast, enums, parser, stream, prettify, printers


@printers.node_printer(ast.CreateEnumStmt, override=True)
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


@printers.node_printer(ast.AlterEnumStmt, override=True)
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


@printers.node_printer(ast.PartitionSpec, override=True)
def partition_spec(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for PartitionSpec."""
    strategy = {
        enums.PartitionStrategy.PARTITION_STRATEGY_LIST: "LIST",
        enums.PartitionStrategy.PARTITION_STRATEGY_RANGE: "RANGE",
        enums.PartitionStrategy.PARTITION_STRATEGY_HASH: "HASH",
    }[node.strategy]
    output.print_symbol(strategy)
    output.write(" ")
    with output.expression(need_parens=True):
        output.print_list(node.partParams)


@printers.node_printer(ast.CreateStmt, override=True)
def create_stmt(  # noqa: C901, PLR0915, PLR0912
    node: ast.Node,
    output: stream.RawStream,
) -> None:
    """Printer for CreateStmt."""
    output.writes("CREATE")
    if isinstance(node.ancestors[0], ast.CreateForeignTableStmt):
        output.writes("FOREIGN")
    elif node.relation.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.writes("TEMPORARY")
    elif node.relation.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.writes("UNLOGGED")
    output.writes("TABLE")
    if node.if_not_exists:
        output.writes("IF NOT EXISTS")
    output.print_node(node.relation)
    if node.ofTypename:
        output.write(" OF ")
        output.print_name(node.ofTypename)
    if node.partbound:
        output.write(" PARTITION OF ")
        output.print_list(node.inhRelations)
    if node.tableElts:
        output.write(" ")
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.tableElts)
            output.newline()
    elif node.partbound:
        output.newline()
        output.write(" ")
    elif not node.ofTypename:
        output.write(" ()")
    with output.push_indent(-1):
        first = True
        if node.inhRelations and not node.partbound:
            output.write(" INHERITS ")
            with output.expression(need_parens=True):
                output.print_list(node.inhRelations)
            first = False
        if node.partbound:
            if first:
                first = False
            else:  # pragma: no cover
                output.newline()
            output.write(" ")
            output.print_node(node.partbound)
        if node.partspec:
            if first:
                first = False
            else:
                output.newline()
            output.newline()
            output.write("PARTITION BY ")
            output.print_node(node.partspec)
        if node.options:
            if first:
                first = False
            else:
                output.newline()
            output.write(" WITH ")
            with output.expression(need_parens=True):
                output.print_list(node.options)
        if node.oncommit != enums.OnCommitAction.ONCOMMIT_NOOP:
            if first:
                first = False
            else:
                output.newline()
            output.write(" ON COMMIT ")
            if node.oncommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
                output.write("PRESERVE ROWS")
            elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
                output.write("DELETE ROWS")
            elif node.oncommit == enums.OnCommitAction.ONCOMMIT_DROP:
                output.write("DROP")
        if node.tablespacename:
            if first:
                first = False
            else:
                output.newline()
            output.write(" TABLESPACE ")
            output.print_name(node.tablespacename)
    if node.accessMethod:
        output.write(" USING ")
        output.print_name(node.accessMethod)


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
