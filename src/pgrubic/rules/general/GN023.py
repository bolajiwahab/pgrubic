"""Checker for DELETE without a WHERE clause."""

from pglast import ast, visitors

from pgrubic.core import linter


class DeleteWithoutWhereClause(linter.BaseChecker):
    """## **What it does**
    Checks for **DELETE** without a **WHERE** clause.

    ## **Why not?**
    Executing a **DELETE** statement without a **WHERE** clause will remove all the rows
    in the table which is most likely an accidental mistake and not what you want.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Add necessary **WHERE** clause.
    """

    def visit_DeleteStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DeleteStmt,
    ) -> None:
        """Visit DeleteStmt."""
        if not node.whereClause:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Found DELETE without a WHERE clause",
                ),
            )
