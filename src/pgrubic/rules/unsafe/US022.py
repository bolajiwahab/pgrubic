"""Checker for rename table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RenameTable(linter.BaseChecker):
    """## **What it does**
    Checks renaming of table.

    ## **Why not?**
    Renaming a table can easily break applications that rely on the table.

    If any part of the application code, database procedures, views, or reports use
    the table, renaming it will cause errors and potentially disrupt business operations.

    ## **When should you?**
    If the table is no longer being accessed by clients, probably after migrating
    clients to a new table.

    ## **Use instead:**
    1. Create a new table with the new name.
    2. Start writing data to the new table.
    3. Copy all data from the old table to the new table.
    4. Migrate clients to the new table.
    """

    def visit_RenameStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if (
            node.renameType == enums.ObjectType.OBJECT_TABLE
            and node.newname != node.relation.relname
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
                    description="Rename table detected",
                    auto_fixable=self.is_auto_fixable,
                    help="Create a new table with the new name",
                ),
            )
