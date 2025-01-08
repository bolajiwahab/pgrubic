"""Checker for insert without target columns."""

from pglast import ast, visitors

from pgrubic.core import linter


class InsertWithoutTargetColumns(linter.BaseChecker):
    """## **What it does**
    Checks for insert without target columns.

    ## **Why not?**
    Specifying the columns in a query explicitly greatly improves clarity and readability.
    This approach helps developers quickly grasp the purpose of a query and fosters
    better collaboration.

    Explicitly listing the target columns can help prevent errors

    ## **When should you?**
    Never.

    ## **Use instead:**
    Specify target columns.
    """

    def visit_InsertStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.InsertStmt,
    ) -> None:
        """Visit InsertStmt."""
        if node.selectStmt and not node.cols:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Insert statement without target columns",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Specify target columns",
                ),
            )
