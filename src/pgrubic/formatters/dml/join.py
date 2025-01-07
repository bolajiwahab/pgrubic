"""Formatter for JOIN statements."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.JoinExpr, override=True)
def join_expr(node: ast.JoinExpr, output: stream.RawStream) -> None:
    """Printer for JoinExpr."""
    indent = (
        -6
        if node.jointype in (enums.JoinType.JOIN_RIGHT, enums.JoinType.JOIN_INNER)
        else -5
    )

    if node.isNatural:
        indent -= 1

    with output.push_indent(indent):
        with output.expression(bool(node.alias)):
            output.print_node(node.larg)
            output.newline()

            if node.isNatural:
                output.write("NATURAL")
                output.space()

            if node.jointype == enums.JoinType.JOIN_INNER:
                if not node.usingClause and not node.quals and not node.isNatural:
                    output.write("CROSS")
                    output.space()
                else:
                    output.write("INNER")
                    output.space()
            elif node.jointype == enums.JoinType.JOIN_LEFT:
                output.write("LEFT")
                output.space()
            elif node.jointype == enums.JoinType.JOIN_FULL:
                output.write("FULL")
                output.space()
            elif node.jointype == enums.JoinType.JOIN_RIGHT:
                output.write("RIGHT")
                output.space()

            output.swrite("JOIN")
            output.space()

            if isinstance(node.rarg, ast.JoinExpr):
                output.indent(3, relative=False)
                # TODO: This needs to be fixed to handle nested JOIN expressions properly  # noqa: TD002, FIX002, TD003, E501
                with output.expression(not bool(node.rarg.alias)):
                    output.indent(4)
                    output.print_node(node.rarg)
                output.newline()
            else:
                output.print_node(node.rarg)

            if node.usingClause:
                output.swrite("USING")
                output.space()
                with output.expression(need_parens=True):
                    output.print_name(node.usingClause, ",")
                if node.join_using_alias:
                    output.space()
                    output.write("AS")
                    output.space()
                    output.print_node(node.join_using_alias)
            elif node.quals:
                output.newline()
                if node.jointype in (
                    enums.JoinType.JOIN_RIGHT,
                    enums.JoinType.JOIN_INNER,
                ):
                    output.space(3)
                else:
                    output.space(2)
                output.swrite("ON")
                output.space()
                output.print_node(node.quals)

        if node.alias:
            output.space()
            output.writes("AS")
            output.space()
            output.print_name(node.alias)

        if isinstance(node.rarg, ast.JoinExpr):
            output.dedent()
