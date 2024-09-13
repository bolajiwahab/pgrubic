"""Checker for missing required columns."""

from pglast import ast, enums, visitors

from pgrubic.core import config, linter


class WronglyTypedRequiredColumn(linter.BaseChecker):
    """## **What it does**
    Checks for wrongly typed required column.

    ## **Why not?**
    If a column has been specified as required with a specific data type and you have
    defined it with a different data type, you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Use the right data type for the required column.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        for column in self.config.lint.required_columns:

            if (
                node.colname == column.name
                and node.typeName.names[-1].sval != column.data_type
            ):

                self.violations.add(
                    linter.Violation(
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        source_text=self.source_text,
                        statement_location=self.statement_location,
                        description=f"Wrongly typed required column `{column.name}`,"
                        f" expected type is `{column.data_type}`",
                    ),
                )

                self._fix(node, column)

    def _fix(self, node: ast.ColumnDef, column: config.Column) -> None:
        """Fix violation."""
        node.typeName = ast.TypeName(
            names=(
                {
                    "@": "String",
                    "sval": column.data_type,
                },
            ),
        )
        node.constraints = (
            *(node.constraints or []),
            ast.Constraint(
                contype=enums.ConstrType.CONSTR_NOTNULL,
            ),
        )
