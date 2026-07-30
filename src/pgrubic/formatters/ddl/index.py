"""Formatter for index."""

import typing

from pglast import ast, printers

from pgrubic.core import formatter
from pgrubic.formatters.ddl import IF_NOT_EXISTS

DEFAULT_INDEX_ACCESS_METHOD: typing.Final[str] = "btree"
DEFAULT_GUTTER: typing.Final[int] = 6


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

    gutter = 10 if node.tableSpace else 7 if node.indexIncludingParams else DEFAULT_GUTTER

    output.newline()
    output.indent(gutter - len("ON"))
    output.write("ON")
    output.space()
    output.print_node(node.relation)

    if (
        node.accessMethod != DEFAULT_INDEX_ACCESS_METHOD
        or not output.config.format.remove_default_index_access_method
    ):
        output.newline()
        output.indent(gutter - len("USING"))
        output.write("USING")
        output.space()
        output.print_name(node.accessMethod)

    output.space()
    output.swrite("(")
    output.print_list(node.indexParams, standalone_items=False)
    output.swrite(")")

    if node.indexIncludingParams:
        output.newline()
        output.indent(gutter - len("INCLUDE"))
        output.write("INCLUDE")
        output.space()
        output.swrite("(")
        output.print_list(node.indexIncludingParams, standalone_items=False)
        output.swrite(")")

    if node.nulls_not_distinct:
        output.newline()
        output.indent(gutter - len("NULLS"))
        output.write("NULLS NOT DISTINCT")

    if node.options:
        output.newline()
        output.indent(gutter - len("WITH"))
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(gutter - len("WITH") + 2)
            output.print_list(node.options, standalone_items=True)
            output.newline()
            output.indent(gutter - len("WITH"))

    if node.tableSpace:
        output.newline()
        output.indent()
        output.write("TABLESPACE")
        output.space()
        output.print_name(node.tableSpace)

    if node.whereClause:
        output.newline()
        output.indent(gutter - len("WHERE"))
        output.write("WHERE")
        output.space()
        output.print_node(node.whereClause)
