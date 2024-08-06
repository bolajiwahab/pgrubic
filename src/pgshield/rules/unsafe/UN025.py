"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class Cluster(linter.Checker):
    """Cluster."""
    is_auto_fixable: bool = False

    def visit_ClusterStmt(
        self,
        ancestors: ast.Node,
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
