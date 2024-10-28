"""Formatter for UPDATE statements."""

from pglast import ast, stream, printers


@printers.node_printer(ast.UpdateStmt, override=True)
def update_stmt(node: ast.UpdateStmt, output: stream.RawStream) -> None:
    """Printer for UpdateStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.newline()
            output.space(2)
            output.indent()

        output.write("UPDATE")
        output.space()
        output.print_node(node.relation)
        output.newline()
        output.space(3)
        output.write("SET")
        output.space()
        output.print_list(node.targetList)
        if node.fromClause:
            output.newline()
            output.space(2)
            output.write("FROM")
            output.space()
            output.print_list(node.fromClause)
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
            first = True
            for elem in node.returningList:
                if first:
                    first = False
                else:
                    output.write(",")
                    output.space()
                output.print_node(elem.val)
                if elem.name:
                    output.space()
                    output.write("AS")
                    output.space()
                    output.print_name(elem.name)
        if node.withClause:
            output.dedent()
