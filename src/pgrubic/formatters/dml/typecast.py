"""Formatter for type casting."""

from pglast import ast, printers

from pgrubic import get_fully_qualified_name
from pgrubic.core import enums, formatter


def native_cast_argument_needs_parentheses(node: ast.Node) -> bool:
    """Check whether a native cast argument needs parentheses."""
    return isinstance(node, ast.A_Expr | ast.BoolExpr)


def is_string_constant(node: ast.Node) -> bool:
    """Check whether a node is a string constant usable as a typed literal."""
    return isinstance(node, ast.A_Const) and isinstance(node.val, ast.String)


@printers.node_printer(ast.TypeCast, override=True)
def type_cast(
    node: ast.TypeCast,
    output: formatter.RawStream,
) -> None:
    """Printer for TypeCast."""
    if (
        is_string_constant(node.arg)
        and isinstance(node.typeName, ast.TypeName)
        and get_fully_qualified_name(node.typeName.names)
        == "pg_catalog.bpchar"  # internal representation of char type
        and node.typeName.typmods is None
    ):
        output.write("char")
        output.space()
        output.print_node(node.arg)
        return

    if output.config.format.type_casting_style == enums.TypeCastingStyle.NATIVE:
        with output.expression(
            need_parens=native_cast_argument_needs_parentheses(node.arg),
        ):
            output.print_node(node.arg)

        output.write("::")
        output.print_node(node.typeName)
        return

    if (
        output.config.format.type_casting_style == enums.TypeCastingStyle.LITERAL
        and is_string_constant(node.arg)
    ):
        output.print_node(node.typeName)
        output.space()
        output.print_node(node.arg)
        return

    output.write("CAST")
    with output.expression(need_parens=True):
        output.print_node(node.arg)
        output.space()
        output.write("AS")
        output.space()
        output.print_node(node.typeName)
