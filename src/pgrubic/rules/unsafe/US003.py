"""Checker for column rename."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ColumnRename(linter.BaseChecker):
    """## **What it does**
    Checks renaming of column.

    ## **Why not?**
    Renaming a column can easily break applications that rely on the column.

    If any part of the application code, database procedures, views, or reports use
    the column, renaming it will cause errors and potentially disrupt business operations.

    ## **When should you?**
    If the column is no longer being referenced by clients, probably after migrating
    clients to a new column.

    ## **Use instead:**
    1. Create a new column with the new name, nullable.
    2. Start writing data to the new column.
    3. Copy all data from the old column to the new column.
    4. Migrate clients to the new column.
    """

    def visit_RenameStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if (
            node.renameType == enums.ObjectType.OBJECT_COLUMN
            and node.newname != node.subname
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Column rename is not safe",
                    auto_fixable=self.is_auto_fixable,
                    help="Create a new column with the new name",
                ),
            )
