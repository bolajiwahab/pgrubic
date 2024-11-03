"""Formatter for INSERT statements."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.InferClause, override=True)
def infer_clause(node: ast.InferClause, output: stream.RawStream) -> None:
    """Printer for InferClause."""
    if node.conname:
        output.swrite("ON CONSTRAINT")
        output.space()
        output.print_name(node.conname)
    if node.indexElems:
        output.separator()
        with output.expression(need_parens=True):
            output.print_list(node.indexElems, standalone_items=False)
    if node.whereClause:
        output.newline()
        output.space()
        output.swrite("WHERE")
        output.space()
        output.print_node(node.whereClause)


@printers.node_printer(ast.OnConflictClause, override=True)
def on_conflict_clause(node: ast.OnConflictClause, output: stream.RawStream) -> None:
    """Printer for OnConflictClause."""
    oca = enums.OnConflictAction
    if node.infer:
        output.print_node(node.infer)
    output.newline()
    if node.action == oca.ONCONFLICT_NOTHING:
        output.space(4)
        output.write("DO NOTHING")
    elif node.action == oca.ONCONFLICT_UPDATE:
        with output.push_indent(4):
            output.write("DO UPDATE SET")
            output.space()
            output.print_list(node.targetList)
            if node.whereClause:
                output.newline()
                output.space(4)
                output.write("WHERE")
                output.space()
                output.print_node(node.whereClause)


@printers.node_printer(ast.InsertStmt, override=True)
def insert_stmt(node: ast.InsertStmt, output: stream.RawStream) -> None:
    """Printer for InsertStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
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
            output.space(4)
            output.write("ON CONFLICT")
            output.space() if node.onConflictClause.infer else output.write("")
            output.print_node(node.onConflictClause)
        if node.returningList:
            output.newline()
            output.write("RETURNING")
            output.space()
            output.print_name(node.returningList, ",")
        if node.withClause:
            output.dedent()
