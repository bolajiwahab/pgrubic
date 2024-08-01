"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class ForbidDeleteWithoutWhereClause(linter.Checker):
    """Forbid delete without where clause."""

    name: str = "unsafe.forbid_delete_without_where_clause"
    code: str = "UN031"

    is_auto_fixable: bool = False

    def visit_DeleteStmt(
        self,
        ancestors: ast.Node,
        node: ast.DeleteStmt,
    ) -> None:
        """Visit DeleteStmt."""
        if node.whereClause is None:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid delete without whereclause",
                ),
            )
