"""Unsafe index operations."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class NonConcurrentIndexDrop(linter.BaseChecker):
    """Non concurrent index drop."""

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent index drop",
                ),
            )

            if self.is_fix_applicable:

                node.concurrent = True
