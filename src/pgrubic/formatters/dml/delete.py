"""Formatters for DELETE statements."""

from pglast import ast, stream, printers


@printers.node_printer(ast.DeleteStmt, override=True)
def delete_stmt(node: ast.DeleteStmt, output: stream.RawStream) -> None:
    """Printer for DeleteStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.indent()

        output.write("DELETE FROM")
        output.space()
        output.print_node(node.relation)
        if node.usingClause:
            output.newline()
            output.space()
            output.write("USING")
            output.space()
            output.print_list(node.usingClause)
        if node.whereClause:
            output.newline()
            output.space()
            output.write("WHERE")
            output.space()
            output.print_node(node.whereClause)
        if node.returningList:
            output.newline()
            output.write("RETURNING")
            output.space()
            output.print_list(node.returningList, standalone_items=False)

        if node.withClause:
            output.dedent()
