"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class ValidatedForeignKeyConstraintOnExistingRows(linter.Checker):
    """Validated foreign key constraint on existing rows."""

    name: str = "unsafe.validated_foreign_key_constraint_on_existing_rows"
    code: str = "USR004"

    is_auto_fixable = True

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Validated foreign key constraint on existing rows",
                ),
            )

            if self.config.fix is True:

                node.skip_validation = True
