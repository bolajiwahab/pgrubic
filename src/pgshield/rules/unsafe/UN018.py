"""Unsafe index operations."""

from pglast import ast, enums

from pgshield.core import linter


class IndexesMovementToTablespace(linter.Checker):
    """Indexes movement to tablespace."""

    name: str = "unsafe.indexes_movement_to_tablespace"
    code: str = "UNI003"

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_INDEX:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Indexes movement to tablespace",
                ),
            )
