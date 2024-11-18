"""Unique constraint creating new index."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class UniqueConstraintCreatingNewIndex(linter.BaseChecker):
    """Unique constraint creating new index."""

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
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Unique constraint creating new index",
                ),
            )
