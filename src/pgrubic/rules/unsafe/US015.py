"""Unique constraint creating new index."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class PrimaryKeyConstraintCreatingNewIndex(linter.BaseChecker):
    """Primary key constraint creating new index."""

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_PRIMARY
            and not node.indexname
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Primary key constraint creating new index",
                ),
            )
