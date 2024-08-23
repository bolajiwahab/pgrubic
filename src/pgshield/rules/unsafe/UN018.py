"""Unsafe index operations."""

from pglast import ast, enums, visitors

from pgshield.core import linter


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
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Indexes movement to tablespace",
                ),
            )
