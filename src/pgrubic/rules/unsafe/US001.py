"""Checker for column drop."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DropColumn(linter.BaseChecker):
    """## **What it does**
    Checks for dropping of column.

    ## **Why not?**
    Not only that mistakenly dropping a column can cause data loss, applications that rely
    on the column will break.

    If any part of the application code, database procedures, views, or reports use
    the column, dropping it will cause errors and potentially disrupt business operations.

    Removing a column from a table may appear to be a reversible action, but it is not.
    Even when you can recover all the data in the column, you cannot restore the column in
    a way that makes the table look exactly as it did before.

    In postgres, **DROP COLUMN** form does not physically remove the column, but simply
    makes it invisible to SQL operations. Subsequent INSERT and UPDATE operations in the
    table will store a NULL value for the column.

    ## **When should you?**
    After updating clients that rely on the column to stop referencing the column and you
    really want to discard the data in the column.

    ## **Use instead:**
    You can either keep the column as nullable or drop it once it is no longer being
    referenced by clients.
    """

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_DropColumn:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Drop column detected",
                ),
            )
