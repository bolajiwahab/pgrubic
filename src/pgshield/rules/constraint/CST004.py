"""Checker for non null column."""
from pglast import ast, enums

from pgshield.core import linter


class NotNullColumn(linter.Checker):
    """## **What it does**
    Checks for nullable required column.

    ## **Why not?**
    If a column has been specified as required then it should not be nullable.
    Having a required column as nullable is an anti-pattern and should be avoided.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Set the required column as **Not Null**
    """

    name: str = "constraint.not_null_column"
    code: str = "CST003"

    is_auto_fixable: bool = True

    def _register_violation(
        self,
        column_name: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.append(
            linter.Violation(
                statement_location=statement_location,
                statement_length=statement_length,
                node_location=node_location,
                description=f"Column '{column_name}' is required as not nullable",
            ),
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors and node.colname in self.config.not_null_columns:

            is_not_null = bool(
                (
                    [
                        constraint
                        for constraint in node.constraints
                        if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                    ]
                    if node.constraints is not None
                    else []
                ),
            )

            if not is_not_null:

                self._register_violation(
                    column_name=node.colname,
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                )

                if self.config.fix is True:

                    node.constraints = (
                        *(node.constraints or []),
                        ast.Constraint(
                            contype=enums.ConstrType.CONSTR_NOTNULL,
                        ),
                    )

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_DropNotNull
            and node.name in self.config.not_null_columns
        ):

            self._register_violation(
                column_name=node.name,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

            if self.config.fix is True and self.config.unsafe_fixes is True:

                node.subtype = enums.AlterTableType.AT_SetNotNull
