"""Checker for cluster."""

from pglast import ast, visitors

from pgrubic.core import linter


class Cluster(linter.BaseChecker):
    """Cluster."""

    def visit_ClusterStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ClusterStmt,
    ) -> None:
        """Visit ClusterStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Cluster found",
            ),
        )
