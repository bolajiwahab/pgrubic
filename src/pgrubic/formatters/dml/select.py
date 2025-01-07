"""Formatter for SELECT statements."""

from pglast import ast, enums, stream, printers


@printers.node_printer(ast.SubLink, override=True)
def sub_link(node: ast.SubLink, output: stream.RawStream) -> None:
    """Printer for SubLink."""
    if node.subLinkType == enums.SubLinkType.EXISTS_SUBLINK:
        output.write("EXISTS")
        output.space()
    elif node.subLinkType == enums.SubLinkType.ALL_SUBLINK:
        output.print_node(node.testexpr)
        output.space()
        output.write(printers.dml.get_string_value(node.operName))
        output.space()
        output.write("ALL")
        output.space()
    elif node.subLinkType == enums.SubLinkType.ANY_SUBLINK:
        output.print_node(node.testexpr)

        if node.operName:
            output.space()
            output.write(printers.dml.get_string_value(node.operName))
            output.space()
            output.write("ANY")
            output.space()
        else:
            output.space()
            output.write("IN")
            output.space()

    elif node.subLinkType == enums.SubLinkType.ARRAY_SUBLINK:
        output.write("ARRAY")
        output.space()
    elif node.subLinkType in (  # pragma: no cover
        enums.SubLinkType.MULTIEXPR_SUBLINK,
        enums.SubLinkType.ROWCOMPARE_SUBLINK,
    ):
        msg = f"SubLink of type {node.subLinkType} not supported yet"
        raise NotImplementedError(msg)

    with output.expression(need_parens=False):
        bool_in_ancestors = ast.BoolExpr in node.ancestors
        nearest_node: ast.Node = abs(node.ancestors).node

        if (
            isinstance(nearest_node, ast.SelectStmt | ast.UpdateStmt | ast.DeleteStmt)
            and nearest_node.whereClause
            or isinstance(nearest_node, ast.A_Expr)
        ):
            indent = 11
            dedent = -4
        elif bool_in_ancestors:
            indent = 8
            dedent = -4
        else:
            indent = 6
            dedent = -4

        with output.push_indent(indent, relative=False):
            output.write("(")
            output.newline()
            output.print_node(node.subselect)
            output.newline()
            output.indent(dedent, relative=False)
            output.write(")")
            output.dedent()


def subexpression_needs_parentheses(node: ast.SelectStmt) -> bool:
    """Check if subexpression needs to be wrapped in parentheses in set operations.
    A SELECT statement on either sides of UNION/INTERSECT/EXCEPT must be wrapped in
    parentheses if it contains ORDER BY/LIMIT/... or is a nested UNION/INTERSECT/EXCEPT.
    """
    return bool(
        node.sortClause
        or node.limitCount
        or node.limitOffset
        or node.lockingClause
        or node.withClause
        or node.op != enums.SetOperation.SETOP_NONE,
    )


@printers.node_printer(ast.SelectStmt, override=True)
def select_stmt(node: ast.SelectStmt, output: stream.RawStream) -> None:
    """Printer for SelectStmt."""
    with output.push_indent():
        if node.withClause:
            output.write("WITH")
            output.space()
            output.print_node(node.withClause)
            output.indent()

        if node.valuesLists:
            with output.expression(need_parens=False):
                output.write("VALUES")
                output.space()
                output.print_lists(node.valuesLists, standalone_items=False)
        elif node.op != enums.SetOperation.SETOP_NONE and (node.larg or node.rarg):
            with output.push_indent():
                if node.larg:
                    with output.expression(
                        subexpression_needs_parentheses(
                            node.larg,
                        ),
                    ):
                        output.print_node(node.larg)

                output.newline()

                if node.op == enums.SetOperation.SETOP_UNION:
                    output.space()
                    if not subexpression_needs_parentheses(node.larg):
                        output.write("UNION")
                    else:
                        output.space()
                        output.write("UNION")
                elif node.op == enums.SetOperation.SETOP_INTERSECT:
                    output.write("INTERSECT")
                elif node.op == enums.SetOperation.SETOP_EXCEPT:
                    output.write("EXCEPT")

                if node.all:
                    output.space()
                    output.write("ALL")

                output.newline()

                if node.rarg:
                    with output.expression(
                        subexpression_needs_parentheses(
                            node.rarg,
                        ),
                    ):
                        output.print_node(node.rarg)
        else:
            output.write("SELECT")
            if node.distinctClause:
                output.space()
                output.write("DISTINCT")

                if node.distinctClause[0]:
                    output.space()
                    output.write("ON")
                    output.space()
                    with output.expression(need_parens=True):
                        output.print_list(node.distinctClause)

                output.newline()
                output.space(6)

            if node.targetList:
                output.space()
                output.print_list(node.targetList)

            if node.intoClause:
                output.newline()
                output.space(2)
                output.write("INTO")
                output.space()

                if node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
                    output.write("UNLOGGED")
                    output.space()
                elif node.intoClause.rel.relpersistence == enums.RELPERSISTENCE_TEMP:
                    output.write("TEMPORARY")
                    output.space()

                output.print_node(node.intoClause)

            if node.fromClause:
                output.newline()
                output.space(2)
                output.write("FROM")
                output.space()
                output.print_list(node.fromClause, standalone_items=True)

            if node.whereClause:
                output.newline()
                output.space()
                output.write("WHERE")
                output.space()
                output.print_node(node.whereClause)

            if node.groupClause:
                output.newline()
                output.space()
                output.write("GROUP BY")
                output.space()

                if node.groupDistinct:
                    output.write("DISTINCT")
                    output.space()

                output.print_list(node.groupClause, standalone_items=True)

            if node.havingClause:
                output.newline()
                output.write("HAVING")
                output.space()
                output.print_node(node.havingClause)

            if node.windowClause:
                output.newline()
                output.write("WINDOW")
                output.space()
                output.print_list(node.windowClause)

        if node.sortClause:
            output.newline()
            output.space()
            output.write("ORDER BY")
            output.space()
            output.print_list(node.sortClause)

        if node.limitCount:
            output.newline()

            if node.limitOption == enums.LimitOption.LIMIT_OPTION_COUNT:
                output.space()
                output.write("LIMIT")
            elif node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space()
                output.write("FETCH FIRST")

            output.space()

            if isinstance(node.limitCount, ast.A_Const) and node.limitCount.isnull:
                output.write("ALL")
            else:
                with output.expression(
                    isinstance(node.limitCount, ast.A_Expr)
                    and node.limitCount.kind == enums.A_Expr_Kind.AEXPR_OP,
                ):
                    output.print_node(node.limitCount)

            if node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space()
                output.write("ROWS WITH TIES")

        if node.limitOffset:
            output.newline()
            output.write("OFFSET")
            output.space()
            output.print_node(node.limitOffset)

        if node.lockingClause:
            output.newline()
            output.write("FOR")
            output.space()
            output.print_list(node.lockingClause)

        if node.withClause:
            output.dedent()


@printers.node_printer(ast.RangeSubselect, override=True)
def range_subselect(node: ast.RangeSubselect, output: stream.RawStream) -> None:
    """Printer for RangeSubselect."""
    if node.lateral:
        output.write("LATERAL")
        output.space()

    with output.push_indent():
        output.write("(")
        output.newline()
        output.space(4)
        output.print_node(node.subquery)
        output.newline()
        output.write(")")

    if node.alias:
        output.space()
        output.write("AS")
        output.space()
        output.print_name(node.alias)
