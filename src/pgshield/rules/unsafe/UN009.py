"""Checker for drop schema."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class DropSchema(linter.BaseChecker):
    """Drop schema."""
    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop schema detected",
                ),
            )
