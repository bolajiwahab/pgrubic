"""Checker for drop tablespace."""

from pglast import ast, visitors

from pgrubic.core import linter


class DropTablespace(linter.BaseChecker):
    """Checks for drop tablespace."""

    def visit_DropTableSpaceStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Drop tablespace detected",
            ),
        )
