"""Formatter for CTEs."""

from pglast import ast, stream, printers


@printers.node_printer(ast.WithClause, override=True)
def with_clause(node: ast.WithClause, output: stream.RawStream) -> None:
    """Printer for WithClause."""
    relindent = -2
    if node.recursive:
        relindent -= output.write("RECURSIVE ")
    output.print_list(node.ctes, relative_indent=relindent, standalone_items=False)


@printers.node_printer(ast.CommonTableExpr, override=True)
def common_table_expr(node: ast.CommonTableExpr, output: stream.RawStream) -> None:
    """Printer for CommonTableExpr."""
    output.print_name(node.ctename)
    if node.aliascolnames:
        with output.expression(need_parens=True):
            if len(node.aliascolnames) > 1:
                output.space(2)
            output.print_name(node.aliascolnames, ",")
        output.indent(amount=-1, relative=False)
        output.newline()

    output.swrite("AS")
    printers.dml.cte_materialize_printer(node.ctematerialized, node, output)
    output.space()
    with output.expression(need_parens=False):
        output.write("(")
        output.newline()
        output.indent(4)
        output.print_node(node.ctequery)
        output.indent(amount=-4, relative=False)
        output.write("\n)")
    if node.search_clause:
        output.newline()
        output.newline()
        output.print_node(node.search_clause)
    if node.cycle_clause:
        output.newline()
        output.newline()
        output.print_node(node.cycle_clause)
    if node.aliascolnames:
        output.dedent()
    output.newline()
