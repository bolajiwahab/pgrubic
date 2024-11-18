"""Checker for drop database."""

from pglast import ast, visitors

from pgrubic.core import linter


class DropDatabase(linter.BaseChecker):
    """Drop database."""

    def visit_DropdbStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Drop database detected",
            ),
        )
