"""Formatter for ALTER ENUM Statements."""

from pglast import ast, stream, printers

from pgrubic.formatters.ddl import IF_NOT_EXISTS


@printers.node_printer(ast.AlterEnumStmt, override=True)
def alter_enum_stmt(node: ast.AlterEnumStmt, output: stream.RawStream) -> None:
    """Printer for AlterEnumStmt."""
    output.write("ALTER TYPE")
    output.space(1)
    output.print_name(node.typeName)
    output.newline()
    output.space(4)
    if node.newVal:
        if node.oldVal:
            output.write("RENAME VALUE")
            output.space(1)
            output.write_quoted_string(node.oldVal)
            output.write("TO")
            output.space(1)
        else:
            output.write("ADD VALUE")
            if node.skipIfNewValExists:
                output.space(1)
                output.write(IF_NOT_EXISTS)
            output.space(1)
        output.write_quoted_string(node.newVal)
    if node.newValNeighbor:
        if node.newValIsAfter:
            output.space(1)
            output.write("AFTER")
            output.space(1)
        else:
            output.space(1)
            output.write("BEFORE")
            output.space(1)
        output.write_quoted_string(node.newValNeighbor)
