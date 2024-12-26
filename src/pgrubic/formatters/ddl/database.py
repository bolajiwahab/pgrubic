"""Formatter for DATABASE Statements."""

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
            if option.lower() in ("encoding", "locale", "strategy"):
                output.write_quoted_string(node.arg.sval.upper())
            else:
                output.write_quoted_string(node.arg.sval)
        else:
            output.print_node(node.arg)


@printers.node_printer(ast.DropdbStmt, override=True)
def drop_db_stmt(node: ast.DropdbStmt, output: stream.RawStream) -> None:
    """Printer for DropdbStmt."""
    output.write("DROP DATABASE")
    if node.missing_ok:
        output.space()
        output.write("IF EXISTS")
    output.space()
    output.print_name(node.dbname)
    if node.options:
        output.newline()
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.options, "")
            output.newline()


@printers.node_printer(ast.DropdbStmt, ast.DefElem, override=True)
def drop_db_stmt_def_elem(node: ast.DefElem, output: stream.RawStream) -> None:
    """Printer for DropdbStmt defelem."""
    output.write(node.defname.upper())
