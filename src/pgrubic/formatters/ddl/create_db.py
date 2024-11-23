"""Formatter for CREATE DATABASE Statements."""

from pglast import ast, stream, printers

from pgrubic import Operators


@printers.node_printer(ast.CreatedbStmt, ast.DefElem, override=True)
def create_db_stmt_def_elem(node: ast.DefElem, output: stream.RawStream) -> None:
    """Printer for CreatedbStmt defelem."""
    option = node.defname
    if option == "connection_limit":
        output.write("CONNECTION LIMIT")
    else:
        output.write(node.defname.upper())
    if node.arg is not None:
        output.space()
        output.write(Operators.EQ)
        output.space()
        if isinstance(node.arg, tuple) or option in ("allow_connections", "is_template"):
            output.write(node.arg.sval)
        elif isinstance(node.arg, ast.String):
            output.write_quoted_string(node.arg.sval)
        else:
            output.print_node(node.arg)
