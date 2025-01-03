"""Formatter for CTEs."""

from pglast import ast, stream, printers


@printers.node_printer(ast.WithClause, override=True)
def with_clause(node: ast.WithClause, output: stream.RawStream) -> None:
    """Printer for WithClause."""
    relative_indent = -2

    if node.recursive:
        relative_indent -= output.write("RECURSIVE ")

    output.print_list(node.ctes, relative_indent=relative_indent, standalone_items=False)


@printers.node_printer(ast.CommonTableExpr, override=True)
def common_table_expr(node: ast.CommonTableExpr, output: stream.RawStream) -> None:
    """Printer for CommonTableExpr."""
    output.print_name(node.ctename)
    if node.aliascolnames:
        output.space()
        with output.expression(need_parens=True):
            output.print_name(node.aliascolnames, ",")
        output.indent(amount=-1, relative=False)

    output.swrite("AS")
    printers.dml.cte_materialize_printer(node.ctematerialized, node, output)
    output.space()

    with output.expression(need_parens=False):
        output.write("(")
        output.newline()
        output.indent(4)
        output.print_node(node.ctequery)
        output.indent(amount=-4, relative=False)
        output.newline()
        output.write(")")

    if node.search_clause:
        output.space()
        output.print_node(node.search_clause)

    if node.cycle_clause:
        output.space()
        output.print_node(node.cycle_clause)
    if node.aliascolnames:
        output.dedent()
    output.newline()
