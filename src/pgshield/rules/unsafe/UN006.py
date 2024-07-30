"""Unsafe column operations."""

from pglast import ast, enums

from pgshield.core import linter


class StoredGeneratedColumn(linter.Checker):
    """Stored generated column."""

    name: str = "unsafe.stored_generated_column"
    code: str = "UN006"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Stored generated column",
                ),
            )
