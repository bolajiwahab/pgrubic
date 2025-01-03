"""Formatter for enum."""

from pglast import ast, stream, printers

from pgrubic.formatters.ddl import IF_NOT_EXISTS


@printers.node_printer(ast.CreateEnumStmt, override=True)
def create_enum_stmt(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for CreateEnumStmt."""
    output.write("CREATE TYPE")
    output.space()
    output.print_name(node.typeName)
    output.write("AS ENUM")
    output.space()
    with output.expression(need_parens=True):
        output.newline()
        output.space(4)
        output.print_list(node.vals, standalone_items=True)
        output.newline()


@printers.node_printer(ast.AlterEnumStmt, override=True)
def alter_enum_stmt(node: ast.AlterEnumStmt, output: stream.RawStream) -> None:
    """Printer for AlterEnumStmt."""
    output.write("ALTER TYPE")
    output.space()
    output.print_name(node.typeName)
    output.newline()
    output.space(4)
    if node.newVal:
        if node.oldVal:
            output.write("RENAME VALUE")
            output.space()
            output.write_quoted_string(node.oldVal)
            output.space()
            output.write("TO")
            output.space()
        else:
            output.write("ADD VALUE")
            if node.skipIfNewValExists:
                output.space()
                output.write(IF_NOT_EXISTS)
            output.space()
        output.write_quoted_string(node.newVal)
    if node.newValNeighbor:
        if node.newValIsAfter:
            output.space()
            output.write("AFTER")
            output.space()
        else:
            output.space()
            output.write("BEFORE")
            output.space()
        output.write_quoted_string(node.newValNeighbor)
