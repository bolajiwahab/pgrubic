"""Formatter for UPDATE statements."""

import typing

from pglast import ast, printers

from pgrubic.core import formatter


@printers.node_printer(ast.UpdateStmt, override=True)
def update_stmt(node: ast.UpdateStmt, output: formatter.PrinterOutput) -> None:
    """Printer for UpdateStmt."""
    target_list = typing.cast(tuple[ast.ResTarget, ...], node.targetList)

    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.indent()

        output.write("UPDATE")
        output.space()
        output.print_node(node.relation)
        output.newline()
        output.space(3)
        output.write("SET")
        output.space()
        output.print_list(target_list, standalone_items=False)

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

        if node.returningClause and node.returningClause.exprs:
            output.newline()
            output.write("RETURNING")
            output.space()
            output.print_list(node.returningClause.exprs)

        if node.withClause:
            output.dedent()
