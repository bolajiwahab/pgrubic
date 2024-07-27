"""Unsafe table operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropTable(linter.Checker):
    """Drop table."""

    name: str = "unsafe.drop_table"
    code: str = "UST001"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop table",
                ),
            )
