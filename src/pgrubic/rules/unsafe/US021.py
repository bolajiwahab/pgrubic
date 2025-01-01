"""Checker for drop table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DropTable(linter.BaseChecker):
    """## **What it does**
    Checks drop table.

    ## **Why not?**
    Not only that mistakenly dropping a table can cause data loss, applications that
    rely on the data will break.

    ## **When should you?**
    If you really want to drop the table.

    ## **Use instead:**
    No suggestions.
    """

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Drop table found",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                ),
            )
