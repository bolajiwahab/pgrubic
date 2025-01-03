"""Checker for drop tablespace."""

from pglast import ast, visitors

from pgrubic.core import linter


class DropTablespace(linter.BaseChecker):
    """## **What it does**
    Checks dropping of tablespace.

    ## **Why not?**
    Not only that mistakenly dropping a tablespace can cause data loss, applications that
    rely on the data will break.

    ## **When should you?**
    If you really want to drop the tablespace.

    ## **Use instead:**
    No suggestions.
    """

    def visit_DropTableSpaceStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        self.violations.add(
            linter.Violation(
                rule_code=self.code,
                rule_name=self.name,
                rule_category=self.category,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Drop tablespace detected",
                is_auto_fixable=self.is_auto_fixable,
                is_fix_enabled=self.is_fix_enabled,
            ),
        )
