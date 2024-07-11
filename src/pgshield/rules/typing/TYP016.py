"""Checker for wrongly typed required columns."""

from pglast import ast

from pgshield import SCHEMA_QUALIFIED_TYPE
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

    name: str = "convention.wrongly_typed_required_column"
    code: str = "TYP016"

    is_auto_fixable = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            is_column_creation(ancestors)
            and node.colname in self.config.required_columns
            and node.typeName.names[-1].sval
            != self.config.required_columns[node.colname]
        ):

            given_type = ".".join(a.sval for a in node.typeName.names)

            expected_type = self.config.required_columns[node.colname].split(".")

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Column '{node.colname}' expected type is"
                    f" '{self.config.required_columns[node.colname]}',"
                    f" found '{given_type}'",
                ),
            )

            if (
                self.config.fix is True
                and len(node.typeName.names) == SCHEMA_QUALIFIED_TYPE
                and len(expected_type) == SCHEMA_QUALIFIED_TYPE
            ):

                node.typeName.names[0].sval = expected_type[0]
                node.typeName.names[1].sval = expected_type[1]
