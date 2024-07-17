"""Checker for wrongly typed required columns."""

from pglast import ast
from pglast.printers import dml

from pgshield import get_full_qualified_type_name
from pgshield.core import linter


class WronglyTypedRequiredColumn(linter.Checker):
    """## **What it does**
    Checks for wrongly typed required columns.

    ## **Why not?**
    If a column has been specified as required and you have typed it wrongly,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Right data types for the required column.
    """

    name: str = "typing.wrongly_typed_required_column"
    code: str = "TYP016"

    is_auto_fixable = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        for column in self.config.required_columns:

            if (
                column.name == node.colname
                and node.typeName.names[-1].sval != column.data_type
            ):

                full_qualified_type_name = get_full_qualified_type_name(
                    node.typeName.names,
                )

                prettified_type = full_qualified_type_name

                if full_qualified_type_name in dml.system_types:

                    prettified_type = dml.system_types[full_qualified_type_name][0]

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Column '{node.colname}' expected type is"
                        f" '{column.data_type}', found"
                        f" '{prettified_type}'",
                    ),
                )

                if self.config.fix is True:

                    node.typeName = ast.TypeName(
                        names=(
                            {
                                "@": "String",
                                "sval": column.data_type,
                            },
                        ),
                    )
