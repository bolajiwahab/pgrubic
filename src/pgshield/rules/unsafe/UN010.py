"""Checker for not null constraint on existing column."""

from pglast import ast, enums

from pgshield.core import linter


class NotNullConstraintOnExistingColumn(linter.Checker):
    """Not null constraint on existing column."""
    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetNotNull:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Not null constraint on existing column",
                ),
            )
