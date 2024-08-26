"""Unsafe constraint operations."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ValidatingForeignKeyConstraintOnExistingRows(linter.BaseChecker):
    """Validating foreign key constraint on existing rows."""

    is_auto_fixable = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Validating foreign key constraint on existing rows",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.Constraint) -> None:
        """Fix violation."""
        node.skip_validation = True
