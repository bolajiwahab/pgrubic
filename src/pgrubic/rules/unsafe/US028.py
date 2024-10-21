"""Checker for non concurrent refresh materialized view."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentRefreshMaterializedView(linter.BaseChecker):
    """Non concurrent refresh materialized view."""

    is_auto_fixable: bool = True

    def visit_RefreshMatViewStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RefreshMatViewStmt,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        if not node.concurrent:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description="Non concurrent refresh materialized view",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.PartitionCmd) -> None:
        """Fix violation."""
        node.concurrent = True
