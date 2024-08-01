"""Unsafe table operations."""

from pglast import ast, enums

from pgshield.core import linter


class TableMovementToTablespace(linter.Checker):
    """Table movement to tablespace."""
    is_auto_fixable: bool = False

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.AlterTableCmd) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[2].stmt.objtype == enums.ObjectType.OBJECT_TABLE
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Table movement to tablespace",
                ),
            )
