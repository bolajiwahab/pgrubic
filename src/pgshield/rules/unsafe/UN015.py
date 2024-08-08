"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class PrimaryKeyConstraintCreatingNewIndex(linter.Checker):
    """Primary key constraint creating new index."""
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableStmt)
            and node.contype == enums.ConstrType.CONSTR_PRIMARY
            and not node.indexname
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Primary key constraint creating new index",
                ),
            )
