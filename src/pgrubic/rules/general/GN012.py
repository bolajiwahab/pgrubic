"""Checker for removal of required columns."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RequiredColumnRemoval(linter.BaseChecker):
    """## **What it does**
    Checks for removal of required columns.

    ## **Why not?**
    If a column has been specified as required and you are removing it from a table,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Leave the required column.

    ## **Configuration**
    `required-columns`: List of required columns along with their data types.
    """

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
                            line_number=self.line_number,
                            column_offset=self.column_offset,
                            statement=self.statement,
                            statement_location=self.statement_location,
                            description=f"Column `{node.name}` is marked as required"
                            " in config",
                        ),
                    )
