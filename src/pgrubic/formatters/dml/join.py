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
    with output.push_indent(amount=indent):
        with output.expression(bool(node.alias)):
            output.print_node(node.larg)
            output.newline()

            if node.isNatural:
                output.write("NATURAL")
                output.space()

            jt = enums.JoinType
            if node.jointype == jt.JOIN_INNER:
                if not node.usingClause and not node.quals and not node.isNatural:
                    output.write("CROSS")
                    output.space()
                else:
                    output.write("INNER")
                    output.space()
            elif node.jointype == jt.JOIN_LEFT:
                output.write("LEFT")
                output.space()
            elif node.jointype == jt.JOIN_FULL:
                output.write("FULL")
                output.space()
            elif node.jointype == jt.JOIN_RIGHT:
                output.write("RIGHT")
                output.space()

            output.swrite("JOIN")
            output.space()

            if isinstance(node.rarg, ast.JoinExpr):
                output.indent(3, relative=False)
                # need this for:
                # tests/test_printers_roundtrip.py::test_pg_regress_corpus[join.sql] -
                # AssertionError: Statement “select * from   int8_tbl x cross join
                # (int4_tbl x cross join lateral (select x.f1) ss)”
                # from libpg_query/test/sql/postgres_regress/join.sql at line 1998
                with output.expression(not bool(node.rarg.alias)):
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
                (
                    output.space(3)
                    if node.jointype
                    in (enums.JoinType.JOIN_RIGHT, enums.JoinType.JOIN_INNER)
                    else output.space(2)
                )
                output.swrite("ON")
                output.space()
                output.print_node(node.quals)

        if node.alias:
            output.newline()
            output.writes("AS")
            output.space()
            output.print_name(node.alias)

        if isinstance(node.rarg, ast.JoinExpr):
            output.dedent()
