"""Checker for drop schema."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DropSchema(linter.BaseChecker):
    """## **What it does**
    Checks dropping of schema.

    ## **Why not?**
    Not only that mistakenly dropping a schema can cause data loss, applications that
    rely on the data will break.

    ## **When should you?**
    If you really want to drop the schema.

    ## **Use instead:**
    No suggestions.
    """

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Drop schema detected",
                    auto_fixable=self.is_auto_fixable,
                ),
            )
