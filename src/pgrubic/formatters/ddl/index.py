"""Formatter for index."""

import typing

from pglast import ast, printers

from pgrubic.core import formatter
from pgrubic.formatters.ddl import IF_NOT_EXISTS

DEFAULT_INDEX_ACCESS_METHOD: typing.Final[str] = "btree"
DEFAULT_GUTTER: typing.Final[int] = 6


@printers.node_printer(ast.IndexStmt, override=True)
def index_stmt(node: ast.IndexStmt, output: formatter.PrinterOutput) -> None:
    """Printer for IndexStmt."""
    index_params = typing.cast(tuple[ast.IndexElem, ...], node.indexParams)
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

    print_access_method = (
        node.accessMethod != DEFAULT_INDEX_ACCESS_METHOD
        or not output.config.format.remove_default_index_access_method
    )

    if print_access_method:
        output.newline()
        output.indent(gutter - len("USING"))
        output.write("USING")
        output.space()
        output.print_name(node.accessMethod)

    output.space()
    output.print_parenthesized_list(
        index_params,
        closing_indent=gutter - len("ON"),
    )

    if node.indexIncludingParams:
        keyword = "INCLUDE"
        output.newline()
        output.indent(gutter - len(keyword))
        output.write(keyword)
        output.space()
        output.print_parenthesized_list(
            node.indexIncludingParams,
            closing_indent=gutter - len(keyword),
        )

    if node.nulls_not_distinct:
        keyword = "NULLS"
        output.newline()
        output.indent(gutter - len(keyword))
        output.write(f"{keyword} NOT DISTINCT")

    if node.options:
        keyword = "WITH"
        output.newline()
        output.indent(gutter - len(keyword))
        output.write(keyword)
        output.space()
        output.print_parenthesized_list(
            node.options,
            closing_indent=gutter - len(keyword),
        )

    if node.tableSpace:
        output.newline()
        output.indent()
        output.write("TABLESPACE")
        output.space()
        output.print_name(node.tableSpace)

    if node.whereClause:
        keyword = "WHERE"
        output.newline()
        output.indent(gutter - len(keyword))
        output.write(keyword)
        output.space()
        output.print_node(node.whereClause)
