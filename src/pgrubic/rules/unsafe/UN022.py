"""Unsafe table operations."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RenameTable(linter.BaseChecker):
    """Rename table."""

    is_auto_fixable: bool = False

    def visit_RenameStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if node.renameType == enums.ObjectType.OBJECT_TABLE:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Rename table",
                ),
            )
