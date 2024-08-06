"""Checker for missing replace in function."""

from pglast import ast

from pgshield.core import linter


class MissingReplaceInFunction(linter.Checker):
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
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if not node.replace and not node.is_procedure:
            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer create or replace for function",
                ),
            )

            if self.config.fix is True:

                node.replace = True
