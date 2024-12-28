"""Checker for table movement to tablespace."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class TableMovementToTablespace(linter.BaseChecker):
    """## **What it does**
    Checks table movement to a tablespace.

    ## **Why not?**
    Moving a table to a different tablespace acquires an **ACCESS EXCLUSIVE** lock on the
    table, blocking other accesses until the movement is completed.
    This will cause downtime if the table is concurrently being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    Have a look at pg_repack as an alternative.
    """

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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Table movement to tablespace",
                    auto_fixable=self.is_auto_fixable,
                    help="Have a look at pg_repack as an alternative",
                ),
            )
