"""Checker for drop tablespace."""

from pglast import ast, visitors

from pgshield.core import linter


class DropTablespace(linter.BaseChecker):
    """Checks for drop tablespace."""
    is_auto_fixable: bool = False

    def visit_DropTableSpaceStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop tablespace detected",
            ),
        )
