"""Printer for AlterOwnerStmt."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.AlterOwnerStmt, override=True)
def alter_owner_stmt(node: ast.AlterOwnerStmt, output: stream.RawStream) -> None:
    """Printer for AlterOwnerStmt."""
    output.write("ALTER")
    output.space()
    output.writes(printers.ddl.OBJECT_NAMES[node.objectType])

    if node.objectType in (
        enums.ObjectType.OBJECT_OPFAMILY,
        enums.ObjectType.OBJECT_OPCLASS,
    ):
        method, *name = node.object
        output.print_name(name)
        output.swrites("USING")
        output.print_symbol(method)
    else:
        output.print_name(node.object)

    output.newline()
    output.space(4)
    output.writes("OWNER TO")
    output.print_node(node.newowner)
