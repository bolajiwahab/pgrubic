"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class TruncateTable(linter.Checker):
    """Truncate table."""

    name: str = "unsafe.truncate_table"
    code: str = "UNT009"

    is_auto_fixable: bool = False

    def visit_TruncateStmt(
        self,
        ancestors: ast.Node,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Truncate table is not safe",
            ),
        )
