"""Checker for wrongly typed required columns."""

from pglast import ast, visitors

from pgshield import get_full_qualified_type_name
from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


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
        if is_column_creation(ancestors):

            for column in self.config.required_columns:

                if (
                    column.name == node.colname
                    and node.typeName.names[-1].sval != column.data_type
                ):

                    print(type(node.typeName.names))

                    self.violations.append(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Column '{node.colname}' expected type is"
                            f" '{column.data_type}', found"
                            f" '{get_full_qualified_type_name(node.typeName.names)}'",
                        ),
                    )

                    # if self.config.fix is True:

                    #     node.tableElts = (
                    #         *node.tableElts,
                    #         ast.ColumnDef(
                    #             colname=column.name,
                    #             typeName=ast.TypeName(
                    #                 names=(
                    #                     {
                    #                         "@": "String",
                    #                         "sval": column.data_type,
                    #                     },
                    #                 ),
                    #             ),
                    #             is_not_null=True,
                    #         ),
                    #     )


                # if self.config.fix is True:
                    # visitors.Delete
                    # node.constraints = (
                    #         *(node.constraints or []),
                    #         ast.Constraint(
                    #             contype=enums.ConstrType.CONSTR_NOTNULL,
                    #         ),
                    #     )

                    # node.typeName = (
                    #     *node.typeName,
                    #     ast.TypeName(
                    #             names=(
                    #                 {
                    #                     "@": "String",
                    #                     "sval": column.data_type,
                    #                 },
                    #             ),
                    #         )
                        # ast.ColumnDef(
                        #     colname=column.name,
                        #     typeName=ast.TypeName(
                        #         names=(
                        #             {
                        #                 "@": "String",
                        #                 "sval": column.data_type,
                        #             },
                        #         ),
                        #     ),
                        #     is_not_null=True,
                        # ),
                    # )
