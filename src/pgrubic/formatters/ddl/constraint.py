"""Formatter for constraint."""

from pglast import ast, enums, printers

from pgrubic import Operators
from pgrubic.core import formatter


@printers.node_printer(ast.Constraint, override=True)
def constraint(node: ast.Constraint, output: formatter.PrinterOutput) -> None:
    """Printer for Constraint."""
    if node.conname:
        output.swrite("CONSTRAINT")
        output.space()
        output.print_name(node.conname)

    # Print the constraint definition
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
        output.space()
        output.write("INCLUDE")
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.including, ",", are_names=True)

    if node.deferrable:
        output.space()
        output.write("DEFERRABLE")
        if node.initdeferred:
            output.swrite("INITIALLY DEFERRED")

    if node.options:
        output.space()
        output.write("WITH")
        output.space()
        with output.expression(need_parens=True):
            output.print_list(node.options)

    if node.indexspace:
        output.space()
        output.writes("USING INDEX TABLESPACE")
        output.print_name(node.indexspace)

    if node.skip_validation:
        output.swrite("NOT VALID")


@printers.node_printer(ast.Constraint, ast.DefElem, override=True)
def constraint_def_elem(node: ast.DefElem, output: formatter.PrinterOutput) -> None:
    """Printer for Constraint defelem."""
    output.print_name(node.defname)
    if node.arg:
        output.write(Operators.EQ)
        output.space()
        output.print_node(node.arg)
