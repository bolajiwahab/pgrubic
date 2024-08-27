"""Unsafe index operations."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class IndexesMovementToTablespace(linter.BaseChecker):
    """Indexes movement to tablespace."""

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_INDEX:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Indexes movement to tablespace",
                ),
            )
