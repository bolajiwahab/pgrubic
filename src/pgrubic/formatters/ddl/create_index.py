"""Formatter for CREATE INDEX statements."""

from pglast import ast, stream, printers

IF_NOT_EXISTS: str = "IF NOT EXISTS"
IF_EXISTS: str = "IF EXISTS"


@printers.node_printer(ast.IndexStmt, override=True)
def index_stmt(node: ast.IndexStmt, output: stream.RawStream) -> None:
    """Printer for IndexStmt."""
    output.write("CREATE")
    output.space(1)
    if node.unique:
        output.write("UNIQUE")
        output.space(1)
    output.write("INDEX")
    output.space(1)
    if node.concurrent:
        output.write("CONCURRENTLY")
        output.space(1)
    if node.if_not_exists:
        output.write(IF_NOT_EXISTS)
        output.space(1)
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
            output.newline()
            output.write("INCLUDE")
            output.space(1)
            output.swrite("(")
            output.print_list(node.indexIncludingParams, standalone_items=False)
            output.swrite(")")
        if node.options:
            output.newline()
            output.write("WITH")
            output.space()
            with output.expression(need_parens=True):
                output.print_list(node.options)
        if node.tableSpace:
            output.newline()
            output.write("TABLESPACE")
            output.space()
            output.print_name(node.tableSpace)
        if node.whereClause:
            output.newline()
            output.write("WHERE")
            output.space()
            output.print_node(node.whereClause)
        if node.nulls_not_distinct:
            output.newline()
            output.write("NULLS NOT DISTINCT")
