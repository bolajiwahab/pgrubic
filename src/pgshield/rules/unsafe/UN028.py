"""Unsafe table operations."""

from pglast import ast, visitors

from pgshield.core import linter


class NonConcurrentRefreshMaterializedView(linter.BaseChecker):
    """Non concurrent refresh materialized view."""
    is_auto_fixable: bool = False

    def visit_RefreshMatViewStmt(
        self,
        ancestors: visitors.Ancestor,
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

            if self.is_fix_applicable:

                node.concurrent = True
