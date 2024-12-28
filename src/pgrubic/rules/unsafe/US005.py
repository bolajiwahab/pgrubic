"""Checker for adding of auto increment identity column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class AddingAutoIncrementIdentityColumn(linter.BaseChecker):
    """## **What it does**
    Checks adding of auto increment identity column.

    ## **Why not?**
    Adding an auto increment identity column to an already populated table will
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
    6. Add a check constraint: **CHECK (column IS NOT NULL) NOT VALID**.
    7. Validate the constraint.
    8. Set the column as NOT NULL
    9. Drop the constraint.
    10. Get the last value of the sequence, with enough offset.
    11. In a single transaction:
        - Drop the default on the new column.
        - Drop the sequence created in step 2.
        - Add GENERATED ALWAYS AS IDENTITY constraint instead,
        specifying the start option as the value from step 10.
    """

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        alter_table_cmd: visitors.Ancestor = ancestors.find_nearest(ast.AlterTableCmd)

        if (
            alter_table_cmd
            and alter_table_cmd.node.subtype == enums.AlterTableType.AT_AddColumn
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
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
                    description="Adding auto increment identity column is not safe",
                    auto_fixable=self.is_auto_fixable,
                    help="Split the operation into multiple steps",
                ),
            )
