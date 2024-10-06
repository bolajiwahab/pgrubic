"""Checker for missing replace in function."""

from pglast import ast, visitors

from pgrubic.core import linter


class MissingReplaceInFunction(linter.BaseChecker):
    """## **What it does**
    Checks for replace in function creation.

    ## **Why not?**
    `CREATE OR REPLACE FUNCTION` simplifies the process of modifying existing functions,
    as you don't need to manually drop and recreate them.

    If you drop and then recreate a function, the new function is not the same entity as
    the old; you will have to drop existing rules, views, triggers, etc. that refer to the
    old function. Use CREATE OR REPLACE FUNCTION to change a function definition without
    breaking objects that refer to the function. It also maintains data integrity and
    consistency.

    ## **When should you?**
    If you don't need to modify an existing function.

    ## **Use instead:**
    CREATE OR REPLACE FUNCTION.
    """

    is_auto_fixable: bool = True

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if not node.replace and not node.is_procedure:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Prefer create or replace for function",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.CreateFunctionStmt) -> None:
        """Fix violation."""
        node.replace = True
