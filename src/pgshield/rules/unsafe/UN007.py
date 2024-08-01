"""Unsafe storage operations."""

from pglast import ast

from pgshield.core import linter


class DropTablespace(linter.Checker):
    """Drop tablespace."""
    is_auto_fixable: bool = False

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop tablespace",
            ),
        )
