"""Checker for adding of auto increment identity column."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class AddingAutoIncrementIdentityColumn(linter.Checker):
    """Forbid adding auto increment identity column."""

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and ancestors.find_nearest(ast.AlterTableCmd).node.subtype
            == enums.AlterTableType.AT_AddColumn
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid adding auto increment identity column",
                ),
            )
