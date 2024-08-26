"""Unsafe index operations."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentIndexCreation(linter.BaseChecker):
    """Non concurrent index creation."""

    is_auto_fixable: bool = True

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if not node.concurrent:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent index creation",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.IndexStmt) -> None:
        """Fix violation."""
        node.concurrent = True
