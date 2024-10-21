"""Checker for table movement to tablespace."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class TableMovementToTablespace(linter.BaseChecker):
    """Table movement to tablespace."""

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors.find_nearest(ast.AlterTableStmt).node.objtype
            == enums.ObjectType.OBJECT_TABLE
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description="Table movement to tablespace",
                ),
            )
