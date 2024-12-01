"""Checker for rename table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RenameTable(linter.BaseChecker):
    """Rename table."""

    def visit_RenameStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if (
            node.renameType == enums.ObjectType.OBJECT_TABLE
            and node.newname != node.relation.relname
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Rename table detected",
                ),
            )
