"""Checker for ID column."""

from pglast import ast, enums

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

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            (
                isinstance(
                    abs(ancestors).node,
                    ast.AlterTableCmd,
                )
                and (abs(ancestors).node.subtype == enums.AlterTableType.AT_AddColumn)
            )
            or isinstance(
                abs(ancestors).node,
                ast.CreateStmt,
            )
        ) and node.colname.lower() == "id":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Use descriptive name for column instead of"
                    f" '{node.colname}'",
                ),
            )

            if self.config.fix is True:

                if isinstance(
                    abs(ancestors).node,
                    ast.AlterTableCmd,
                ):

                    table = ancestors.parent.parent.node.relation.relname

                if isinstance(abs(ancestors).node, ast.CreateStmt):

                    table = ancestors.parent.node.relation.relname

                node.colname = table + "_" + node.colname
