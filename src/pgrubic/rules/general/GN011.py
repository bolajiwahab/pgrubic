"""Checker for missing required columns."""

from pglast import ast, enums, visitors

from pgrubic.core import config, linter
from pgrubic.rules.general import get_columns_from_table_creation


class MissingRequiredColumn(linter.BaseChecker):
    """## **What it does**
    Checks for required columns.

    ## **Why not?**
    If a column has been specified as required and you have not defined it,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Define the required columns.
    """

    is_auto_fixable: bool = True

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if not node.partbound and node.tableElts:

            given_columns, _ = get_columns_from_table_creation(node)

            for column in self.config.lint.required_columns:

                if column.name not in given_columns:

                    self.violations.add(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Column '{column.name}' of type"
                            f" '{column.data_type}' is marked as required in config",
                        ),
                    )

                    self._fix(node, column)

    def _fix(self, node: ast.CreateStmt, column: config.RequiredColumns) -> None:
        """Fix violation."""
        node.tableElts = (
            *node.tableElts,
            ast.ColumnDef(
                colname=column.name,
                typeName=ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": column.data_type,
                        },
                    ),
                ),
                constraints=(
                    *(node.constraints or []),
                    ast.Constraint(
                        contype=enums.ConstrType.CONSTR_NOTNULL,
                    ),
                ),
            ),
        )
