"""Checker for adding of auto increment column."""

from pglast import ast, visitors

from pgrubic.core import linter


class AddingAutoIncrementColumn(linter.BaseChecker):
    """## **What it does**
    Checks adding of auto increment column.

    ## **Why not?**
    Adding an auto increment column to an already populated table will
    have to backfill the newly added column, causing the table to be locked
    in which no other operations can be performed on the table for the duration
    of the backfill. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Create a new column typed bigint, nullable.
    2. Create a sequence.
    3. Set the next value of the sequence to the total number of rows in the table
       with enough offset.
    4. Set the default value of the new column to the next value of the sequence.
    5. Backfill the new column for all existing rows.
    6. If the new column is to be set as not null,
       add a check constraint: **CHECK (column IS NOT NULL) NOT VALID**
    7. Validate the constraint.
    8. Set the column as NOT NULL.
    9. Drop the constraint.
    """

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and (
            node.typeName.names[-1].sval in ["smallserial", "serial", "bigserial"]
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
                    description="Adding auto increment column is not safe",
                    auto_fixable=self.is_auto_fixable,
                    help="Split the operation into multiple steps",
                ),
            )
