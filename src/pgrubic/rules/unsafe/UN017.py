"""Unsafe index operations."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class IndexMovementToTablespace(linter.BaseChecker):
    """Index movement to tablespace."""

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors.find_nearest(ast.AlterTableStmt).node.objtype
            == enums.ObjectType.OBJECT_INDEX
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Index movement to tablespace",
                ),
            )
