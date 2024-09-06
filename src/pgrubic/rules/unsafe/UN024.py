"""Checker for tables movement to tablespace."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class TablesMovementToTablespace(linter.BaseChecker):
    """Tables movement to tablespace."""

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if (
            node.objtype == enums.ObjectType.OBJECT_TABLE
            and node.new_tablespacename != node.orig_tablespacename
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Tables movement to tablespace",
                ),
            )
