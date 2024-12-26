"""Formatter for CONSTRAINT."""

from pglast import ast, enums, stream, printers

from pgrubic import Operators


@printers.node_printer(ast.Constraint, override=True)
def constraint(node: ast.Constraint, output: stream.RawStream) -> None:
    """Printer for Constraint."""
    if node.conname:
        output.swrite("CONSTRAINT")
        output.space()
        output.print_name(node.conname)
        output.newline()
        output.indent(8)

    printers.ddl.constr_type_printer(node.contype, node, output)

    if node.indexname:
        output.space()
        output.write("USING INDEX")
        output.space()
        output.print_name(node.indexname)

    if node.keys and node.contype in (
        enums.ConstrType.CONSTR_UNIQUE,
        enums.ConstrType.CONSTR_PRIMARY,
    ):
        output.space()
        with output.expression(need_parens=True):
            output.print_name(node.keys, ",")

    if node.including:
        output.newline()
        output.write("INCLUDE")
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.including, ",", are_names=True)

    if node.deferrable:
        output.newline()
        output.swrite("DEFERRABLE")
        if node.initdeferred:
            output.swrite("INITIALLY DEFERRED")

    if node.options:
        output.newline()
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.newline()
            output.space(4)
            output.print_list(node.options)
            output.newline()

    if node.indexspace:
        output.newline()
        output.writes("USING INDEX TABLESPACE")
        output.print_name(node.indexspace)

    if node.skip_validation:
        output.swrite("NOT VALID")


@printers.node_printer(ast.Constraint, ast.DefElem, override=True)
def constraint_def_elem(node: ast.DefElem, output: stream.RawStream) -> None:
    """Printer for Constraint defelem."""
    output.print_name(node.defname)
    if node.arg:
        output.write(Operators.EQ)
        output.space()
        output.print_node(node.arg)
