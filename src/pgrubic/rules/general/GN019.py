"""Checker for unlogged table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class UnloggedTable(linter.BaseChecker):
    """## **What it does**
    Checks for use of unlogged tables.

    ## **Why not?**
    Unlogged tables are not crash-safe: an unlogged table is automatically truncated after
    a crash or unclean shutdown. The contents of an unlogged table are also not replicated
    to standby servers.
    Any indexes created on an unlogged table are automatically unlogged as well. Any
    sequences created together with the unlogged table (for identity or serial columns)
    are also created as unlogged.

    ## **When should you?**
    The table is transient and its content can be regenerated after a crash or unclean
    shutdown.

    ## **Use instead:**
    Use a regular table instead.
    """

    is_auto_fixable: bool = True

    description: str = "Prefer regular table to unlogged table"

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.relation.relpersistence == enums.RELPERSISTENCE_UNLOGGED:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=self.description,
                ),
            )

            self._fix_create_unlogged_table(node)

    def _fix_create_unlogged_table(self, node: ast.CreateStmt) -> None:
        """Fix violation."""
        node.relation.relpersistence = enums.RELPERSISTENCE_PERMANENT

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetUnLogged:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=self.description,
                ),
            )

            self._fix_alter_unlogged_table(node)

    def _fix_alter_unlogged_table(self, node: ast.AlterTableCmd) -> None:
        """Fix violation."""
        node.subtype = enums.AlterTableType.AT_SetLogged
