"""Formatter for INSERT statements."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.InsertStmt, override=True)
def insert_stmt(node: ast.InsertStmt, output: stream.RawStream) -> None:
    """Printer for InsertStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.newline()
            output.space(2)
            output.indent()

        output.write("INSERT INTO")
        output.space()
        output.print_node(node.relation)
        if node.cols:
            output.space()
            with output.expression(need_parens=True):
                output.print_list(node.cols, standalone_items=False)
        else:
            output.separator()
        if node.override:
            if node.override == enums.OverridingKind.OVERRIDING_USER_VALUE:
                output.space()
                output.write("OVERRIDING USER VALUE")
                output.space()
            elif node.override == enums.OverridingKind.OVERRIDING_SYSTEM_VALUE:
                output.space()
                output.write("OVERRIDING SYSTEM VALUE")
                output.space()
        if node.selectStmt:
            output.newline()
            output.print_node(node.selectStmt)
        else:
            output.write("DEFAULT VALUES")
        if node.onConflictClause:
            output.newline()
            output.write("ON CONFLICT")
            output.space()
            output.print_node(node.onConflictClause)
        if node.returningList:
            output.newline()
            output.write("RETURNING")
            output.space()
            output.print_name(node.returningList, ",")

        if node.withClause:
            output.dedent()
