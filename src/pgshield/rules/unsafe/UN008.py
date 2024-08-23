"""Checker for drop database."""

from pglast import ast, visitors

from pgshield.core import linter


class DropDatabase(linter.BaseChecker):
    """Drop database."""
    is_auto_fixable: bool = False

    def visit_DropdbStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop database detected",
            ),
        )
