"""Formatter for type casting."""

import typing

from pglast import ast, printers

from pgrubic import get_fully_qualified_name
from pgrubic.core import enums, formatter

NATIVE_CAST_OPERATOR = "::"


def native_cast_argument_needs_parentheses(
    node: ast.Node,
    output: formatter.PrinterOutput,
) -> bool:
    """Check whether a native cast argument needs parentheses."""
    if isinstance(node, ast.FuncCall):
        function_name = get_fully_qualified_name(
            typing.cast(tuple[ast.String, ...], node.funcname),
        )
        return output.get_printer_for_function(function_name) is not None

    return not isinstance(
        node,
        ast.A_ArrayExpr
        | ast.A_Const
        | ast.A_Indirection
        | ast.ColumnRef
        | ast.ParamRef
        | ast.TypeCast,
    )


def is_string_constant(node: ast.Node) -> bool:
    """Check whether a node is a string constant usable as a typed literal."""
    return isinstance(node, ast.A_Const) and isinstance(node.val, ast.String)


def is_char_type(node: ast.Node) -> bool:
    """Check whether a node is PostgreSQL's internal char type."""
    return (
        isinstance(node, ast.TypeName)
        and node.names is not None
        and get_fully_qualified_name(node.names) == "pg_catalog.bpchar"
    )


def is_native_cast(
    node: ast.TypeCast,
    output: formatter.PrinterOutput,
) -> bool:
    """Check whether a cast originated from PostgreSQL's ``::`` syntax."""
    native_cast_operator_length = len(NATIVE_CAST_OPERATOR)
    return (
        output.source_code is not None
        and node.location is not None
        and output.source_code[
            node.location : node.location + native_cast_operator_length
        ]
        == NATIVE_CAST_OPERATOR
    )


def char_has_default_length(typmods: tuple[ast.Node, ...]) -> bool:
    """Check whether a char type has the implicit default length of one."""
    default_char_length = 1
    typmod = typmods[0]
    return (
        isinstance(typmod, ast.A_Const)
        and isinstance(typmod.val, ast.Integer)
        and typmod.val.ival == default_char_length
    )


@printers.node_printer(ast.TypeCast, override=True)
def type_cast(
    node: ast.TypeCast,
    output: formatter.PrinterOutput,
) -> None:
    """Printer for TypeCast."""
    argument = typing.cast(ast.Expr, node.arg)
    type_name = typing.cast(ast.TypeName, node.typeName)
    # An unmodified CHAR typed literal is not interchangeable with an implicit
    # char cast: CHAR 'xyz' retains all three characters, while both
    # CAST('xyz' AS char) and 'xyz'::char mean char(1). PostgreSQL represents
    # the typed literal with typmods=None, so preserve that form and only
    # convert other char casts to literal syntax when they have a safe,
    # explicit non-default length.
    if (
        is_string_constant(argument)
        and is_char_type(type_name)
        and type_name.typmods is None
    ):
        output.write("char")
        output.space()
        output.print_node(argument)
        return

    if output.config.format.type_casting_style == enums.TypeCastingStyle.NATIVE:
        with output.expression(
            need_parens=native_cast_argument_needs_parentheses(argument, output),
        ):
            output.print_node(argument)

        output.write(NATIVE_CAST_OPERATOR)
        output.print_node(type_name)
        return

    if (
        output.config.format.type_casting_style == enums.TypeCastingStyle.LITERAL
        and is_string_constant(argument)
        and (
            not is_char_type(type_name)
            or (
                type_name.typmods is not None
                and not char_has_default_length(type_name.typmods)
            )
        )
    ):
        output.print_node(type_name)
        output.space()
        output.print_node(argument)
        return

    if (
        output.config.format.type_casting_style == enums.TypeCastingStyle.LITERAL
        and is_native_cast(node, output)
    ):
        with output.expression(
            need_parens=native_cast_argument_needs_parentheses(argument, output),
        ):
            output.print_node(argument)
        output.write(NATIVE_CAST_OPERATOR)
        output.print_node(type_name)
        return

    output.write("CAST")
    with output.expression(need_parens=True):
        output.print_node(argument)
        output.space()
        output.write("AS")
        output.space()
        output.print_node(type_name)
