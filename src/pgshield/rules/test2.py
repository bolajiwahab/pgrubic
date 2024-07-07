from pglast import parse_sql, visitors, ast

class ForbidRedefinitionOfTableColumn(visitors.Visitor):
    """Forbid redefinition of table column."""

    name: str = "convention.forbid_redefinition_of_table_column"
    code: str = "CVG011"

    is_auto_fixable: bool = True

    def visit_RawStmt(
        self,
        ancestors: ast.Node,
        node: ast.RawStmt,
    ) -> None:
        """Visit CreateStmt."""
        print(node)



sql_code = """
select a = null;
"""

print(ForbidRedefinitionOfTableColumn()(parse_sql(sql_code)))
