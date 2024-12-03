"""Checker for missing replace in trigger."""

from pglast import ast, visitors

from pgrubic.core import linter


class MissingReplaceInFunction(linter.BaseChecker):
    """## **What it does**
    Checks for replace in trigger creation.

    ## **Why not?**
    `CREATE OR REPLACE TRIGGER` simplifies the process of modifying existing functions,
    as you don't need to manually drop and recreate them.

    If you drop and then recreate a trigger, the new trigger is not the same entity as
    the old; you will have to drop existing rules, views, triggers, etc. that refer to the
    old trigger. Use CREATE OR REPLACE TRIGGER to change a trigger definition without
    breaking objects that refer to the trigger. It also maintains data integrity and
    consistency.

    ## **When should you?**
    If you don't need to modify an existing trigger.

    ## **Use instead:**
    CREATE OR REPLACE TRIGGER.
    """

    is_auto_fixable: bool = True

    def visit_CreateTrigStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateTrigStmt,
    ) -> None:
        """Visit CreateTrigStmt."""
        if not node.replace:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Prefer create or replace for trigger",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.CreateTrigStmt) -> None:
        """Fix violation."""
        node.replace = True
