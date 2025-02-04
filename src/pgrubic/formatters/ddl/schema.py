"""Printers for SchemaStmt."""

from pglast import ast, enums, stream, printers

from pgrubic.formatters.ddl import IF_EXISTS, IF_NOT_EXISTS


@printers.node_printer(ast.CreateSchemaStmt, override=True)
def create_schema_stmt(node: ast.CreateSchemaStmt, output: stream.RawStream) -> None:
    """Print a CreateSchemaStmt node."""
    output.writes("CREATE SCHEMA")

    if node.if_not_exists:
        output.writes(IF_NOT_EXISTS)

    if node.schemaname:
        output.print_name(node.schemaname)

    if node.authrole:
        output.newline()
        output.space(4)
        output.swrites("AUTHORIZATION")
        output.print_node(node.authrole)

    if node.schemaElts:
        output.newline()
        output.space(4)
        with output.push_indent():
            output.print_list(node.schemaElts, "", standalone_items=True)


@printers.node_printer(ast.AlterObjectSchemaStmt, override=True)
def alter_object_schema_stmt(
    node: ast.AlterObjectSchemaStmt,
    output: stream.RawStream,
) -> None:
    """Print an AlterObjectSchemaStmt node."""
    objtype = node.objectType
    output.writes("ALTER")
    output.writes(printers.ddl.OBJECT_NAMES[objtype])

    if node.missing_ok:
        output.writes(IF_EXISTS)

    if objtype in {
        enums.ObjectType.OBJECT_FOREIGN_TABLE,
        enums.ObjectType.OBJECT_MATVIEW,
        enums.ObjectType.OBJECT_SEQUENCE,
        enums.ObjectType.OBJECT_TABLE,
        enums.ObjectType.OBJECT_VIEW,
    }:
        output.print_name(node.relation)
    elif objtype in (enums.ObjectType.OBJECT_OPCLASS, enums.ObjectType.OBJECT_OPFAMILY):
        method, *name = node.object
        output.print_name(name)
        output.swrites("USING")
        output.print_symbol(method)
    else:
        output.print_name(node.object)

    output.newline()
    output.space(4)
    output.swrites("SET SCHEMA")
    output.print_name(node.newschema)
