"""Formatter for database."""

import typing

from pglast import ast, printers

from pgrubic import Operators
from pgrubic.core import formatter


@printers.node_printer(ast.CreatedbStmt, ast.DefElem, override=True)
def create_db_stmt_def_elem(
    node: ast.DefElem,
    output: formatter.PrinterOutput,
) -> None:
    """Printer for CreatedbStmt defelem."""
    option = typing.cast(str, node.defname)
    label = "CONNECTION LIMIT" if option == "connection_limit" else option
    output.write_keyword(label)
    output.space()
    output.write(Operators.EQ)
    output.space()

    if node.arg is None:
        output.write("DEFAULT")
    elif isinstance(node.arg, ast.String):
        value = typing.cast(str, node.arg.sval)

        if option in ("allow_connections", "is_template"):
            output.write(value)
        else:
            output.write_quoted_string(value)
    else:
        output.print_node(node.arg)


@printers.node_printer(ast.DropdbStmt, override=True)
def drop_db_stmt(node: ast.DropdbStmt, output: formatter.PrinterOutput) -> None:
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
def drop_db_stmt_def_elem(node: ast.DefElem, output: formatter.PrinterOutput) -> None:
    """Printer for DropdbStmt defelem."""
    option = typing.cast(str, node.defname)
    output.write_keyword(option)
