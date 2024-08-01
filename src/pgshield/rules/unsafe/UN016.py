"""Unsafe index operations."""

from pglast import ast

from pgshield.core import linter


class NonConcurrentIndexCreation(linter.Checker):
    """Non concurrent index creation."""

    name: str = "unsafe.non_concurrent_index_creation"
    code: str = "UN016"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent index creation",
                ),
            )
