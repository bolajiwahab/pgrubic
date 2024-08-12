"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class NonConcurrentRefreshMaterializedView(linter.Checker):
    """Non concurrent refresh materialized view."""
    is_auto_fixable: bool = False

    def visit_RefreshMatViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.RefreshMatViewStmt,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        if not node.concurrent:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent refresh materialized view",
                ),
            )

            if self.can_apply_fix:

                node.concurrent = True
