"""Checker for existence of not null constraint on required columns."""

from pglast import ast, enums

from pgshield.core import linter


class NullableRequiredColumn(linter.Checker):
    """## **What it does**
    Checks for existence of not null constraint on required columns.

    ## **Why not?**
    If a column has been specified as required then it should not be nullable.
    Having a required column as nullable is an anti-pattern and should be avoided.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Set the required column as **Not Null**.
    """

    name: str = "general.remove_not_null_from_required_column"
    code: str = "GN013"

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        for column in self.config.required_columns:

            if node.colname == column.name:

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

                    self.violations.append(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Column '{node.colname}' is marked as required"
                            " in config",
                        ),
                    )

                    if self.config.fix is True:

                        node.constraints = (
                            *(node.constraints or []),
                            ast.Constraint(
                                contype=enums.ConstrType.CONSTR_NOTNULL,
                            ),
                        )