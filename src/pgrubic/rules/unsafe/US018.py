"""Indexes movement to tablespace."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class IndexesMovementToTablespace(linter.BaseChecker):
    """Indexes movement to tablespace."""

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if (
            node.objtype == enums.ObjectType.OBJECT_INDEX
            and node.new_tablespacename != node.orig_tablespacename
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Indexes movement to tablespace",
                ),
            )
