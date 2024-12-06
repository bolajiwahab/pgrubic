"""Checker for wrongly typed required columns."""

from pglast import ast, visitors
from pglast.printers import dml

from pgrubic import get_fully_qualified_name
from pgrubic.core import config, linter


class WronglyTypedRequiredColumn(linter.BaseChecker):
    """## **What it does**
    Checks for wrongly typed required columns.

    ## **Why not?**
    If a column has been specified as required and you have typed it wrongly,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Right data types for the required column.

    ## **Configuration**
    `required-columns`: List of required columns along with their data types.
    """

    is_auto_fixable = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        for column in self.config.lint.required_columns:
            if column.name == node.colname:
                fully_qualified_type_name = get_fully_qualified_name(
                    node.typeName.names,
                )

                prettified_type = fully_qualified_type_name

                if fully_qualified_type_name in dml.system_types:
                    prettified_type = dml.system_types[fully_qualified_type_name][0]

                if column.data_type != prettified_type:
                    self.violations.add(
                        linter.Violation(
                            rule=self.code,
                            line_number=self.line_number,
                            column_offset=self.column_offset,
                            line=self.line,
                            statement_location=self.statement_location,
                            description=f"Column '{node.colname}' expected type is"
                            f" '{column.data_type}', found"
                            f" '{prettified_type}'",
                            auto_fixable=self.is_auto_fixable,
                            help="Use the right data type for the required column",
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
