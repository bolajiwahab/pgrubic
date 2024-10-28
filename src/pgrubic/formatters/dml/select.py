"""Formatter for SELECT statements."""

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
                output.space(3)
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


@printers.node_printer(ast.BoolExpr, override=True)
def bool_expr(node: ast.BoolExpr, output: stream.RawStream) -> None:
    """Printer for BoolExpr."""
    bet = enums.BoolExprType
    in_res_target = isinstance(node.ancestors[0], ast.ResTarget)
    needs = ast.BoolExpr in node.ancestors
    if node.boolop == bet.AND_EXPR:
        indent_value = -4 if not in_res_target else None
        relindent = -5 if needs and not in_res_target else indent_value
        output.print_list(
            node.args,
            "AND",
            relative_indent=relindent,
            item_needs_parens=printers.dml._bool_expr_needs_to_be_wrapped_in_parens,  # noqa: SLF001
        )
    elif node.boolop == bet.OR_EXPR:
        relindent = -3 if not in_res_target else None
        output.print_list(
            node.args,
            "OR",
            relative_indent=relindent,
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


@printers.node_printer(ast.SelectStmt, override=True)
def select_stmt(node: ast.SelectStmt, output: stream.RawStream) -> None:
    """Printer for SelectStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH ")
            output.print_node(node.withClause)
            output.newline()
            output.space(2)
            output.indent()

        so = enums.SetOperation

        if node.valuesLists:
            # Is this a SELECT ... FROM (VALUES (...))?
            with output.expression(isinstance(node.ancestors[0], ast.RangeSubselect)):
                output.write("VALUES ")
                output.print_lists(node.valuesLists, standalone_items=False)
        elif node.op != so.SETOP_NONE and (node.larg or node.rarg):
            with output.push_indent():
                if node.larg:
                    with output.expression(
                        printers.dml._select_needs_to_be_wrapped_in_parens(  # noqa: SLF001
                            node.larg,
                        ),
                    ):
                        output.print_node(node.larg)
                output.newline()
                output.newline()
                if node.op == so.SETOP_UNION:
                    output.write("UNION")
                elif node.op == so.SETOP_INTERSECT:
                    output.write("INTERSECT")
                elif node.op == so.SETOP_EXCEPT:
                    output.write("EXCEPT")
                if node.all:
                    output.write(" ALL")
                output.newline()
                if node.rarg:
                    with output.expression(
                        printers.dml._select_needs_to_be_wrapped_in_parens(  # noqa: SLF001
                            node.rarg,
                        ),
                    ):
                        output.print_node(node.rarg)
        else:
            output.write("SELECT")
            if node.distinctClause:
                output.write(" DISTINCT")
                if node.distinctClause[0]:
                    output.write(" ON ")
                    with output.expression(need_parens=True):
                        output.print_list(node.distinctClause)
                output.newline()
                output.space(6)
            if node.targetList:
                output.space()
                output.print_list(node.targetList)
            if node.intoClause:
                output.newline()
                output.write("INTO ")
                if node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
                    output.write("UNLOGGED ")
                elif node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_TEMP:
                    output.write("TEMPORARY ")
                output.print_node(node.intoClause)
            if node.fromClause:
                output.newline()
                output.space(2)
                output.write("FROM ")
                output.print_list(node.fromClause)
            if node.whereClause:
                output.newline()
                output.space()
                output.write("WHERE ")
                output.print_node(node.whereClause)
            if node.groupClause:
                output.newline()
                output.space()
                output.write("GROUP BY ")
                if node.groupDistinct:
                    output.write("DISTINCT ")
                output.print_list(node.groupClause)
            if node.havingClause:
                output.newline()
                output.write("HAVING ")
                output.print_node(node.havingClause)
            if node.windowClause:
                output.newline()
                output.write("WINDOW ")
                output.print_list(node.windowClause)
        if node.sortClause:
            output.newline()
            output.space()
            output.write("ORDER BY ")
            output.print_list(node.sortClause)
        if node.limitCount:
            output.newline()
            if node.limitOption == enums.LimitOption.LIMIT_OPTION_COUNT:
                output.space()
                output.write("LIMIT ")
            elif node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space()
                output.write("FETCH FIRST ")
            if isinstance(node.limitCount, ast.A_Const) and node.limitCount.isnull:
                output.write("ALL")
            else:
                with output.expression(
                    isinstance(node.limitCount, ast.A_Expr)
                    and node.limitCount.kind == enums.A_Expr_Kind.AEXPR_OP,
                ):
                    output.print_node(node.limitCount)
            if node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.write(" ROWS WITH TIES ")
        if node.limitOffset:
            output.newline()
            output.write("OFFSET ")
            output.print_node(node.limitOffset)
        if node.lockingClause:
            output.newline()
            output.write("FOR ")
            output.print_list(node.lockingClause)

        if node.withClause:
            output.dedent()


@printers.node_printer(ast.IntoClause, override=True)
def into_clause(node: ast.IntoClause, output: stream.RawStream) -> None:
    """Printer for IntoClause."""
    output.print_node(node.rel)
    if node.colNames:
        output.write(" ")
        with output.expression(need_parens=True):
            output.print_name(node.colNames, ",")
    output.newline()
    with output.push_indent(2):
        if node.accessMethod:
            output.write("USING ")
            output.print_name(node.accessMethod)
            output.newline()
        if node.options:
            output.write("WITH ")
            with output.expression(need_parens=True):
                output.print_list(node.options)
            output.newline()
        if node.onCommit != enums.OnCommitAction.ONCOMMIT_NOOP:
            output.space(2)
            output.write("ON COMMIT ")
            if node.onCommit == enums.OnCommitAction.ONCOMMIT_PRESERVE_ROWS:
                output.write("PRESERVE ROWS")
            elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DELETE_ROWS:
                output.write("DELETE ROWS")
            elif node.onCommit == enums.OnCommitAction.ONCOMMIT_DROP:
                output.write("DROP")
            output.newline()
        if node.tableSpaceName:
            output.write("TABLESPACE ")
            output.print_name(node.tableSpaceName)
            output.newline()
