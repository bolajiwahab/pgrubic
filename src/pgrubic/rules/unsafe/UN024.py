"""Unsafe table operations."""

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
        if node.objtype == enums.ObjectType.OBJECT_TABLE:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Tables movement to tablespace",
                ),
            )
