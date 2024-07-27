"""Unsafe storage operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropDatabase(linter.Checker):
    """Drop database."""

    name: str = "unsafe.drop_database"
    code: str = "UNS002"

    is_auto_fixable: bool = False

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop database",
            ),
        )
