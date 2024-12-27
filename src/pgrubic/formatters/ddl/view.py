"""Formatter for view."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.ViewStmt, override=True)
def view_stmt(node: ast.ViewStmt, output: stream.RawStream) -> None:
    """Printer for ViewStmt."""
    output.write("CREATE")
    output.space()
    if node.replace:
        output.write("OR REPLACE")
        output.space()
    if node.view.relpersistence == enums.RELPERSISTENCE_TEMP:
        output.write("TEMPORARY")
        output.space()
    elif node.view.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
        output.write("UNLOGGED")
        output.space()
    output.write("VIEW")
    output.space()
    output.print_node(node.view)
    if node.aliases:
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.aliases, are_names=True)
    output.space()
    if node.options:
        output.write("WITH ")
        with output.expression(need_parens=True):
            output.print_list(node.options)
        output.newline()
        output.space(2)
    output.write("AS")
    output.newline()
    with output.push_indent():
        output.print_node(node.query)
    printers.ddl.view_check_option_printer(node.withCheckOption, node, output)
