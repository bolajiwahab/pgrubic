"""DML formatter."""

from pglast import ast, enums, stream, printers


def _select_needs_to_be_wrapped_in_parens(node: ast.SelectStmt) -> bool:
    # Accordingly with https://www.postgresql.org/docs/current/sql-select.html, a SELECT
    # statement on either sides of UNION/INTERSECT/EXCEPT must be wrapped in parens if it
    # contains ORDER BY/LIMIT/... or is a nested UNION/INTERSECT/EXCEPT
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
                output.print_lists(node.valuesLists)
        elif node.op != so.SETOP_NONE and (node.larg or node.rarg):
            with output.push_indent():
                if node.larg:
                    with output.expression(
                        _select_needs_to_be_wrapped_in_parens(node.larg),
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
                output.newline()
                if node.rarg:
                    with output.expression(
                        _select_needs_to_be_wrapped_in_parens(node.rarg),
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
            if node.targetList:
                output.write(" ")
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
                output.space(1)
                output.write("WHERE ")
                output.print_node(node.whereClause)
            if node.groupClause:
                output.newline()
                output.space(1)
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
            output.space(1)
            output.write("ORDER BY ")
            output.print_list(node.sortClause)
        if node.limitCount:
            output.newline()
            if node.limitOption == enums.LimitOption.LIMIT_OPTION_COUNT:
                output.space(1)
                output.write("LIMIT ")
            elif node.limitOption == enums.LimitOption.LIMIT_OPTION_WITH_TIES:
                output.space(1)
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
