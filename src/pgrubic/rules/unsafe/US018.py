"""Indexes movement to tablespace."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class IndexesMovementToTablespace(linter.BaseChecker):
    """## **What it does**
    Checks indexes movement to a different tablespace.

    ## **Why not?**
    Moving indexes to a different tablespace acquires an **ACCESS EXCLUSIVE** lock on the
    respective tables, blocking other accesses until the movement is completed.
    This will cause downtime if the tables are concurrently being accessed by other
    clients.

    ## **When should you?**
    If the tables are empty.
    If the tables are not empty but is not being concurrently accessed.

    ## **Use instead:**
    Have a look at pg_repack as an alternative.
    """

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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Indexes movement to tablespace",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Have a look at pg_repack as an alternative",
                ),
            )
