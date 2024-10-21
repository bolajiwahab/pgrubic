"""Checker for drop table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DropTable(linter.BaseChecker):
    """Drop table."""

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description="Drop table found",
                ),
            )
