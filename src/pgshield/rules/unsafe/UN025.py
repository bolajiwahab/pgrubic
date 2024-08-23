"""Unsafe table operations."""

from pglast import ast, visitors

from pgshield.core import linter


class Cluster(linter.BaseChecker):
    """Cluster."""
    is_auto_fixable: bool = False

    def visit_ClusterStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ClusterStmt,
    ) -> None:
        """Visit ClusterStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Cluster",
            ),
        )
