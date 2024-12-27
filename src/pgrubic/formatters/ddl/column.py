"""Formatter for column."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.ColumnDef, override=True)
def column_def(node: ast.ColumnDef, output: stream.RawStream) -> None:
    """Printer for ColumnDef."""
    if node.colname:
        output.print_name(node.colname)
        output.space()

    if node.typeName:
        output.print_name(node.typeName)
        if node.storage_name:
            output.write("STORAGE")
            output.space()
            output.write(node.storage_name)

        if node.compression:
            output.space()
            output.write("COMPRESSION")
            output.space()
            output.print_name(node.compression)
    elif node.constraints:
        output.write("WITH OPTIONS")
        output.space()

    if node.fdwoptions:
        output.space()
        output.write("OPTIONS")
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.fdwoptions, ",")

    if node.collClause:
        output.print_node(node.collClause)

    if node.constraints:
        # move NOT NULL constraint to the end
        constraints = [
            x for x in node.constraints if x.contype != enums.ConstrType.CONSTR_NOTNULL
        ] + [x for x in node.constraints if x.contype == enums.ConstrType.CONSTR_NOTNULL]
        output.print_list(constraints, "", standalone_items=False)
