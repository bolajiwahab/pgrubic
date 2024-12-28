"""Checker for usage of AStar."""

from pglast import ast, visitors

from pgrubic.core import linter


class AStar(linter.BaseChecker):
    """## **What it does**
    Checks for usage of asterisk (*) in column references.

    ## **Why not?**
    Specifying the columns in a query explicitly greatly improves clarity and readability.
    This approach helps developers quickly grasp the purpose of the query and fosters
    better collaboration.

    Also, using (SELECT *) complicates code maintenance. When the table structure
    changes, such as adding, renaming, or removing columns, queries with SELECT * can
    fail unexpectedly or silently return incorrect results.
    By explicitly listing the necessary columns, you ensure the code is more resilient to
    changes in the database schema.

    ## **When should you?**
    Almost Never.

    ## **Use instead:**
    Name Columns Explicitly.
    """

    def visit_A_Star(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Star,
    ) -> None:
        """Visit A_Star."""
        if ancestors.find_nearest(ast.SelectStmt):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Asterisk in column reference is discouraged",
                    auto_fixable=self.is_auto_fixable,
                    help="Name columns explicitly",
                ),
            )
