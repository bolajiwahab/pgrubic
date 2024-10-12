"""Checker for truncate table."""

from pglast import ast, visitors

from pgrubic.core import linter


class TruncateTable(linter.BaseChecker):
    """Truncate table."""

    def visit_TruncateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        self.violations.add(
            linter.Violation(
                line_number=self.line_number,
                column_offset=self.column_offset,
                statement=self.statement,
                statement_location=self.statement_location,
                description="Truncate table detected",
            ),
        )
