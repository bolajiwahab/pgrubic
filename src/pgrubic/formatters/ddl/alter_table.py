"""Formatter for ALTER TABLE Statements."""

from pglast import ast, stream, printers

from pgrubic.formatters.ddl import IF_EXISTS


@printers.node_printer(ast.AlterTableStmt, override=True)
def alter_table_stmt(node: ast.AlterTableStmt, output: stream.RawStream) -> None:
    """Printer for AlterTableStmt."""
    output.write("ALTER")
    output.space(1)
    output.writes(printers.ddl.OBJECT_NAMES[node.objtype])
    if node.missing_ok:
        output.write(IF_EXISTS)
    output.space(1)
    output.print_node(node.relation)
    output.newline()
    output.space(4)
    if len(node.cmds) > 1:
        with output.push_indent():
            output.print_list(node.cmds, ",")
    else:
        output.print_list(node.cmds, ",", standalone_items=True)
