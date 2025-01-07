"""Formatter for rename."""

from pglast import ast, enums, stream, printers
from pglast.printers.ddl import OBJECT_NAMES


@printers.node_printer(ast.RenameStmt, override=True)
def rename_stmt(node: ast.RenameStmt, output: stream.RawStream) -> None:
    """Printer for RenameStmt."""
    objtype = node.renameType
    output.write("ALTER")
    output.space()
    if objtype == enums.ObjectType.OBJECT_TABCONSTRAINT:
        output.write("TABLE")
    elif objtype == enums.ObjectType.OBJECT_DOMCONSTRAINT:  # pragma: no cover
        output.write("DOMAIN")
    elif objtype == enums.ObjectType.OBJECT_ROLE:  # pragma: no cover
        output.write("ROLE")
    else:
        output.write(
            OBJECT_NAMES[
                (
                    node.relationType
                    if objtype
                    in (enums.ObjectType.OBJECT_ATTRIBUTE, enums.ObjectType.OBJECT_COLUMN)
                    else objtype
                )
            ],
        )
    output.space()

    if node.missing_ok:
        output.write("IF EXISTS")
        output.space()

    if objtype in (
        enums.ObjectType.OBJECT_SCHEMA,
        enums.ObjectType.OBJECT_DATABASE,
        enums.ObjectType.OBJECT_ROLE,
        enums.ObjectType.OBJECT_TABLESPACE,
    ):
        output.print_name(node.subname)
    elif objtype in (  # pragma: no cover
        enums.ObjectType.OBJECT_RULE,
        enums.ObjectType.OBJECT_POLICY,
        enums.ObjectType.OBJECT_TRIGGER,
    ):
        output.print_name(node.subname)
        output.space()
        output.write("ON")
        output.space()
        output.print_node(node.relation)
    elif node.relation:
        output.print_node(node.relation)
    elif objtype in (
        enums.ObjectType.OBJECT_OPFAMILY,
        enums.ObjectType.OBJECT_OPCLASS,
    ):  # pragma: no cover
        method, *name = node.object
        output.print_name(name)
        output.space()
        output.write("USING")
        output.space()
        output.print_symbol(method)
    else:
        output.print_name(node.object)
    output.newline()
    output.indent(4)
    output.write("RENAME")
    output.space()

    if objtype == enums.ObjectType.OBJECT_COLUMN:
        output.write("COLUMN")
        output.space()
        output.print_name(node.subname)
    elif objtype == enums.ObjectType.OBJECT_TABCONSTRAINT:
        output.write("CONSTRAINT")
        output.space()
        output.print_name(node.subname)
    elif objtype == enums.ObjectType.OBJECT_ATTRIBUTE:  # pragma: no cover
        output.write("ATTRIBUTE")
        output.space()
        output.print_name(node.subname)
    elif objtype == enums.ObjectType.OBJECT_DOMCONSTRAINT:  # pragma: no cover
        output.writes("CONSTRAINT")
        output.print_name(node.subname)

    output.swrite("TO")
    output.space()
    output.print_name(node.newname)

    if node.behavior == enums.DropBehavior.DROP_CASCADE:  # pragma: no cover
        output.space()
        output.write("CASCADE")
