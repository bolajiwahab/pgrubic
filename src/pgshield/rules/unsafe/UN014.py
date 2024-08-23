"""Unsafe constraint operations."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class UniqueConstraintCreatingNewIndex(linter.BaseChecker):
    """Unique constraint creating new index."""
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Unique constraint creating new index",
                ),
            )
