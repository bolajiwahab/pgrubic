"""Unsafe storage operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropSchema(linter.Checker):
    """Drop schema."""

    name: str = "unsafe.drop_schema"
    code: str = "UN009"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop schema is not safe",
                ),
            )
