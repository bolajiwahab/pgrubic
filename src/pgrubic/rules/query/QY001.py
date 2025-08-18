"""Checker for ordinal number group by."""

from pglast import ast, visitors

from pgrubic.core import linter


class OrdinalNumberGroupBy(linter.BaseChecker):
    """## **What it does**
    Checks that GROUP BY does not use numeric ordinals (e.g., GROUP BY 1).

    ## **Why not?**
    Using ordinals reduces readability, makes queries fragile when the **SELECT** list
    changes, and obscures intent.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Explicit column names or expressions.
    """

    def visit_SelectStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.SelectStmt,
    ) -> None:
        """Visit SelectStmt."""
        if node.groupClause and any(
            isinstance(column, ast.A_Const) and isinstance(column.val, ast.Integer)
            for column in node.groupClause
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
                    description="Ordinal numbers in GROUP BY",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use explicit column names or expressions instead",
                ),
            )
