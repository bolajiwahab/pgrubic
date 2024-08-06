"""Unsafe storage operations."""

from pglast import ast

from pgshield.core import linter


class DropDatabase(linter.Checker):
    """Drop database."""
    is_auto_fixable: bool = False

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop database",
            ),
        )
