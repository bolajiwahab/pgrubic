"""Unsafe table operations."""

from pglast import ast, enums

from pgshield.core import linter


class TablesMovementToTablespace(linter.Checker):
    """Tables movement to tablespace."""

    name: str = "unsafe.tables_movement_to_tablespace"
    code: str = "UST004"

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Tables movement to tablespace",
                ),
            )
