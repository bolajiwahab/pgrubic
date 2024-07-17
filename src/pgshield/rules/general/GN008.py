"""Checker for missing replace in procedure."""

from pglast import ast

from pgshield.core import linter


class MissingReplaceInProcedure(linter.Checker):
    """## **What it does**
    Checks for replace in procedure creation.

    ## **Why not?**
    `CREATE OR REPLACE PROCEDURE` simplifies the process of modifying existing procedures,
    as you don't need to manually drop and recreate them.

    If you drop and then recreate a procedure, the new procedure is not the same entity as
    the old; you will have to drop existing rules, views, triggers, etc. that refer to the
    old procedure. Use CREATE OR REPLACE PROCEDURE to change a procedure definition
    without breaking objects that refer to the procedure. It also maintains data integrity
    and consistency.

    ## **When should you?**
    If you don't need to modify an existing procedure.

    ## **Use instead:**
    CREATE OR REPLACE PROCEDURE.
    """

    name: str = "general.missing_replace_in_procedure"
    code: str = "GN008"

    is_auto_fixable: bool = True

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if not node.replace and node.is_procedure:
            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer replace for procedure",
                ),
            )

            if self.config.fix is True:

                node.replace = True
