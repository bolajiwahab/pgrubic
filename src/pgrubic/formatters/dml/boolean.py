"""Formatter for boolean expressions."""

from pglast import ast, enums, stream, printers


def bool_expr_needs_to_be_wrapped_in_parens(node: ast.BoolExpr) -> bool:
    """Check if the node needs to be wrapped in parens."""
    return isinstance(node, ast.BoolExpr) and node.boolop in (
        enums.BoolExprType.AND_EXPR,
        enums.BoolExprType.OR_EXPR,
    )


@printers.node_printer(ast.BoolExpr, override=True)
def bool_expr(node: ast.BoolExpr, output: stream.RawStream) -> None:
    """Printer for BoolExpr."""
    in_target_list = isinstance(node.ancestors[0], ast.ResTarget)
    bool_expr_in_ancestors = ast.BoolExpr in node.ancestors

    if node.boolop == enums.BoolExprType.AND_EXPR:
        indent_value = -4 if not in_target_list else None
        relative_indent = (
            -5 if bool_expr_in_ancestors and not in_target_list else indent_value
        )
        output.print_list(
            node.args,
            "AND",
            relative_indent=relative_indent,
            item_needs_parens=bool_expr_needs_to_be_wrapped_in_parens,
        )
    elif node.boolop == enums.BoolExprType.OR_EXPR:
        relative_indent = -3 if not in_target_list else None
        output.print_list(
            node.args,
            "OR",
            relative_indent=relative_indent,
            item_needs_parens=bool_expr_needs_to_be_wrapped_in_parens,
        )
    else:
        output.writes("NOT")
        with output.expression(
            bool_expr_needs_to_be_wrapped_in_parens(
                node.args[0],
            ),
        ):
            output.print_node(node.args[0])
