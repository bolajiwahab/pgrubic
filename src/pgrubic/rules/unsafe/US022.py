"""Checker for rename table."""

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
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Rename table detected",
                ),
            )
