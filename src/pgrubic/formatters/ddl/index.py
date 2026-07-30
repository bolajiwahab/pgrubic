"""Formatter for index."""

import typing

from pglast import ast, printers

from pgrubic.core import formatter
from pgrubic.formatters.ddl import IF_NOT_EXISTS

DEFAULT_INDEX_ACCESS_METHOD: typing.Final[str] = "btree"


@printers.node_printer(ast.IndexStmt, override=True)
def index_stmt(node: ast.IndexStmt, output: formatter.IndentedStream) -> None:
    """Printer for IndexStmt."""
    output.write("CREATE")
    output.space()

    if node.unique:
        output.write("UNIQUE")
        output.space()

    output.write("INDEX")

    if node.concurrent:
        output.space()
        output.write("CONCURRENTLY")

    if node.if_not_exists:
        output.space()
        output.write(IF_NOT_EXISTS)

    if node.idxname:
        output.space()
        output.print_name(node.idxname)

    output.newline()

    with output.push_indent(4):
        output.write("ON")
        output.space()
        output.print_node(node.relation)

        if (
            node.accessMethod != DEFAULT_INDEX_ACCESS_METHOD
            or not output.config.format.remove_default_index_access_method
        ):
            output.newline()
            output.indent(1)
            output.write("USING")
            output.space()
            output.print_name(node.accessMethod)

        output.space()
        output.swrite("(")
        output.print_list(node.indexParams, standalone_items=False)
        output.swrite(")")

        if node.indexIncludingParams:
            output.space()
            output.write("INCLUDE")
            output.space()
            output.swrite("(")
            output.print_list(node.indexIncludingParams, standalone_items=False)
            output.swrite(")")

        if node.nulls_not_distinct:
            output.newline()
            output.indent(1)
            output.write("NULLS NOT DISTINCT")

        if node.options:
            output.newline()
            output.indent(2)
            output.write("WITH")
            output.space()
            with output.expression(need_parens=True):
                output.print_list(node.options, standalone_items=False)

        if node.tableSpace:
            output.newline()
            output.indent()
            output.write("TABLESPACE")
            output.space()
            output.print_name(node.tableSpace)

        if node.whereClause:
            output.newline()
            output.indent(1)
            output.write("WHERE")
            output.space()
            output.print_node(node.whereClause)
