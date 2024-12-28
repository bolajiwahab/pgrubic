"""Unique constraint creating new index."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class UniqueConstraintCreatingNewIndex(linter.BaseChecker):
    """## **What it does**
    Checks unique constraint creating new index.

    ## **Why not?**
    Unique constraint is supported by a unique index in the background.
    Adding a unique constraint to an already populated table will create a unique index
    in non-concurrent mode, scanning and validating that there are no violating records
    in the table. This causes the table to be locked, in which no other operations can be
    performed on the table for the duration of the validation. This will cause downtime if
    the table is concurrently being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Create a unique index in concurrent mode:
        **CREATE UNIQUE INDEX CONCURRENTLY .. ON .. (..)**.
    2. Add the unique constraint using the index created in step 1:
        **ALTER TABLE .. ADD CONSTRAINT .. UNIQUE USING INDEX ..**
    """

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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Unique constraint creating new index",
                    auto_fixable=self.is_auto_fixable,
                    help="Create a unique index in concurrent mode, then add the unique constraint using the index",  # noqa: E501
                ),
            )
