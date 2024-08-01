"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class ForbidUpdateWithoutWhereClause(linter.Checker):
    """Forbid update without where clause."""
    is_auto_fixable: bool = False

    def visit_UpdateStmt(
        self,
        ancestors: ast.Node,
        node: ast.UpdateStmt,
    ) -> None:
        """Visit UpdateStmt."""
        if node.whereClause is None:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid update without whereclause",
                ),
            )
