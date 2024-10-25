"""Formatter for CREATE ENUM Statements."""

from pglast import ast, stream, printers


@printers.node_printer(ast.CreateEnumStmt, override=True)
def create_enum_stmt(node: ast.Node, output: stream.RawStream) -> None:
    """Printer for CreateEnumStmt."""
    output.write("CREATE TYPE")
    output.space(1)
    output.print_name(node.typeName)
    output.write("AS ENUM")
    output.space(1)
    output.write("")
    with output.expression(need_parens=True):
        output.newline()
        output.space(4)
        output.print_list(node.vals, standalone_items=True)
        output.newline()
