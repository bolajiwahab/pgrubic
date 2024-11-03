"""Formatter for boolean expressions."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.BoolExpr, override=True)
def bool_expr(node: ast.BoolExpr, output: stream.RawStream) -> None:
    """Printer for BoolExpr."""
    bet = enums.BoolExprType
    in_res_target = isinstance(node.ancestors[0], ast.ResTarget)
    bool_in_ancestors = ast.BoolExpr in node.ancestors
    if node.boolop == bet.AND_EXPR:
        indent_value = -4 if not in_res_target else None
        relative_indent = -5 if bool_in_ancestors and not in_res_target else indent_value
        output.print_list(
            node.args,
            "AND",
            relative_indent=relative_indent,
            item_needs_parens=printers.dml._bool_expr_needs_to_be_wrapped_in_parens,  # noqa: SLF001
        )
    elif node.boolop == bet.OR_EXPR:
        relative_indent = -3 if not in_res_target else None
        output.print_list(
            node.args,
            "OR",
            relative_indent=relative_indent,
            item_needs_parens=printers.dml._bool_expr_needs_to_be_wrapped_in_parens,  # noqa: SLF001
        )
    else:
        output.writes("NOT")
        with output.expression(
            printers.dml._bool_expr_needs_to_be_wrapped_in_parens(  # noqa: SLF001
                node.args[0],
            ),
        ):
            output.print_node(node.args[0])
