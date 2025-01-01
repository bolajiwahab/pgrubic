"""Formatter for renme."""

from pglast import ast, enums, stream, printers
from pglast.printers.ddl import OBJECT_NAMES


@printers.node_printer(ast.RenameStmt, override=True)
def rename_stmt(node: ast.RenameStmt, output: stream.RawStream) -> None:
    """Printer for RenameStmt."""
    object_type = enums.ObjectType
    objtype = node.renameType
    output.write("ALTER ")
    if objtype == object_type.OBJECT_TABCONSTRAINT:
        output.write("TABLE")
    elif objtype == object_type.OBJECT_DOMCONSTRAINT:
        output.write("DOMAIN")
    elif objtype == object_type.OBJECT_ROLE:
        output.write("ROLE")
    else:
        output.write(
            OBJECT_NAMES[
                (
                    node.relationType
                    if objtype
                    in (object_type.OBJECT_ATTRIBUTE, object_type.OBJECT_COLUMN)
                    else objtype
                )
            ],
        )
    output.write(" ")
    if node.missing_ok:
        output.write("IF EXISTS ")
    if objtype in (
        object_type.OBJECT_SCHEMA,
        object_type.OBJECT_DATABASE,
        object_type.OBJECT_ROLE,
        object_type.OBJECT_TABLESPACE,
    ):
        output.print_name(node.subname)
    elif objtype in (
        object_type.OBJECT_RULE,
        object_type.OBJECT_POLICY,
        object_type.OBJECT_TRIGGER,
    ):
        output.print_name(node.subname)
        output.write(" ON ")
        output.print_node(node.relation)
    elif node.relation:
        output.print_node(node.relation)
    elif objtype in (object_type.OBJECT_OPFAMILY, object_type.OBJECT_OPCLASS):
        method, *name = node.object
        output.print_name(name)
        output.write(" USING ")
        output.print_symbol(method)
    else:
        output.print_name(node.object)
    output.newline()
    output.indent(4)
    output.write("RENAME")
    output.space()
    if objtype == object_type.OBJECT_COLUMN:
        output.write("COLUMN ")
        output.print_name(node.subname)
    elif objtype == object_type.OBJECT_TABCONSTRAINT:
        output.write("CONSTRAINT ")
        output.print_name(node.subname)
    elif objtype == object_type.OBJECT_ATTRIBUTE:
        output.write("ATTRIBUTE ")
        output.print_name(node.subname)
    elif objtype == object_type.OBJECT_DOMCONSTRAINT:
        output.writes("CONSTRAINT")
        output.print_name(node.subname)
    output.swrite("TO ")
    output.print_name(node.newname)
    if node.behavior == enums.DropBehavior.DROP_CASCADE:
        output.write(" CASCADE")
