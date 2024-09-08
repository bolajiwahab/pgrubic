"""Checker for cluster."""

from pglast import ast, visitors

from pgrubic.core import linter


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
                line_number=self.line_number,
                column_offset=self.column_offset,
                source_text=self.source_text,
                statement_location=self.statement_location,
                description="Cluster found",
            ),
        )
