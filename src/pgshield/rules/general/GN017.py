"""Checker for ID column."""

from pglast import ast

from pgshield.core import linter


class IdColumn(linter.Checker):
    """## **What it does**
    Checks for usage of ID columns.

    ## **Why not?**
    The name "id" does not provide much information about what the column represents in
    the context of the table as it is so genric. Using a more descriptive name can improve
    clarity, readability, and maintainability of the database schema.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Descriptive name.
    """

    name: str = "general.id_column"
    code: str = "GN017"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.colname.lower() == "id":

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Use descriptive name for column instead of"
                    f" '{node.colname}'",
                ),
            )
