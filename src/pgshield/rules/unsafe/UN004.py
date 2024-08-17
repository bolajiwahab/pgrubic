"""Checker for adding of auto increment column."""

from pglast import ast, visitors

from pgshield.core import linter


class AddingAutoIncrementColumn(linter.Checker):
    """Forbid adding auto increment column."""

    is_auto_fixable: bool = False

    def visit_ColumnDef(self, ancestors: visitors.Ancestor, node: ast.ColumnDef) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and (
            node.typeName.names[-1].sval in ["smallserial", "serial", "bigserial"]
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid adding auto increment column",
                ),
            )
