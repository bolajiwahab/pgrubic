"""Unsafe table operations."""

from pglast import ast, visitors

from pgshield.core import linter


class TruncateTable(linter.BaseChecker):
    """Truncate table."""
    is_auto_fixable: bool = False

    def visit_TruncateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Truncate table is not safe",
            ),
        )
