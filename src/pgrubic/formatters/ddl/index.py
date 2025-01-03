"""Formatter for index."""

from pglast import ast, stream, printers

from pgrubic.formatters.ddl import IF_NOT_EXISTS


@printers.node_printer(ast.IndexStmt, override=True)
def index_stmt(node: ast.IndexStmt, output: stream.RawStream) -> None:
    """Printer for IndexStmt."""
    output.write("CREATE")
    output.space()

    if node.unique:
        output.write("UNIQUE")
        output.space()

    output.write("INDEX")
    output.space()

    if node.concurrent:
        output.write("CONCURRENTLY")
        output.space()

    if node.if_not_exists:
        output.write(IF_NOT_EXISTS)
        output.space()

    if node.idxname:
        output.print_name(node.idxname)

    output.newline()

    with output.push_indent(4):
        output.write("ON")
        output.space()
        output.print_node(node.relation)

        if node.accessMethod != "btree":
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
