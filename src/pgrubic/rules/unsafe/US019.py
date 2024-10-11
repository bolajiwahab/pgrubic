"""Non concurrent index drop."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NonConcurrentIndexDrop(linter.BaseChecker):
    """Non concurrent index drop."""

    is_auto_fixable: bool = True

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Non concurrent index drop",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.DropStmt) -> None:
        """Fix violation."""
        node.concurrent = True
