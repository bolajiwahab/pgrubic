"""Checker for truncate table."""

from pglast import ast, visitors

from pgrubic.core import linter


class TruncateTable(linter.BaseChecker):
    """## **What it does**
    Checks truncating of table.

    ## **Why not?**
    Truncating a table can easily break applications that rely on the data in the table.

    If any part of the application code, database procedures, views, or reports use
    the data, truncating it will cause errors and potentially disrupt business operations.

    ## **When should you?**
    If the data in the table is no longer needed by clients, probably a test data.

    ## **Use instead:**
    No suggestions.
    """

    def visit_TruncateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Truncate table detected",
                auto_fixable=self.is_auto_fixable,
            ),
        )
