"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class ValidatedCheckConstraintOnExistingRows(linter.Checker):
    """Validated check constraint on existing rows."""
    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Validated check constraint on existing rows",
                ),
            )

            if self.is_fix_applicable:

                node.skip_validation = True
