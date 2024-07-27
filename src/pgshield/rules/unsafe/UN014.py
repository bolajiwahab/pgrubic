"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class UniqueConstraintCreatingNewIndex(linter.Checker):
    """Unique constraint creating new index."""

    name: str = "unsafe.unique_constraint_creating_new_index"
    code: str = "USR006"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Unique constraint creating new index",
                ),
            )
