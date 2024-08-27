"""Checker for removal of required columns."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RemoveRequiredColumn(linter.BaseChecker):
    """## **What it does**
    Checks for removal of required columns.

    ## **Why not?**
    If a column has been specified as required and you are removing it from a table,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Leave the required column.
    """

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_DropColumn:

            for column in self.config.lint.required_columns:

                if node.name == column.name:

                    self.violations.add(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Column {node.name} is marked as required"
                            " in config",
                        ),
                    )
