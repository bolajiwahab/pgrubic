"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class NotNullOnExistingColumn(linter.Checker):
    """Not null on existing column."""

    name: str = "unsafe.not_null_on_existing_column"
    code: str = "UN010"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetNotNull:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Not null on existing column",
                ),
            )
