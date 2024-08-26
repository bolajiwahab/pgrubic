"""Unsafe table operations."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DropTable(linter.BaseChecker):
    """Drop table."""

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop table found",
                ),
            )
