"""Checker for constant generated columns."""

from pglast import ast, enums

from pgshield.core import linter


class ConstantGeneratedColumn(linter.Checker):
    """## **What it does**
    Checks for usage of constant generated columns.

    ## **Why not?**
    Always generating a constant value for a column is not useful and only leads to
    duplicated data all over the place and wastage of storage.

    ## **When should you?**
    If the table will be storing just one row at any point in time.

    ## **Use instead:**
    Generated column with expression.
    """
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_GENERATED and isinstance(
            node.raw_expr,
            ast.A_Const,
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Constant generated column found",
                ),
            )
