"""Checker for ordinal number order by."""

from pglast import ast, visitors

from pgrubic.core import linter


class OrdinalNumberOrderBy(linter.BaseChecker):
    """## **What it does**
    Checks that ORDER BY does not use numeric ordinals (e.g., ORDER BY 1).

    ## **Why not?**
    Using ordinals reduces readability, makes queries fragile when the **SELECT** list
    changes, and obscures intent.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Explicit column names or expressions.
    """

    @staticmethod
    def _is_ordinal_sort_column(column: ast.SortBy) -> bool:
        """Check for ordinal sort column."""
        return isinstance(column.node, ast.A_Const) and isinstance(
            column.node.val,
            ast.Integer,
        )

    def visit_SelectStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.SelectStmt,
    ) -> None:
        """Visit SelectStmt."""
        if node.sortClause and any(
            isinstance(column, ast.SortBy) and self._is_ordinal_sort_column(column)
            for column in node.sortClause
        ):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Ordinal numbers in ORDER BY",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use explicit column names or expressions instead",
                ),
            )
