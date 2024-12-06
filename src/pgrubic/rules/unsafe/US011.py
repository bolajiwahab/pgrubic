"""Checker for not null constraint on new column with volatile default."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NotNullConstraintOnNewColumnWithVolatileDefault(linter.BaseChecker):
    """## **What it does**
    Checks **NOT NULL** constraint on a new column with volatile default.

    ## **Why not?**
    Adding a new column with **NOT NULL** constraint and a volatile default to an already
    populated table will have to backfill the newly added column with the default, causing
    the table to be locked, in which no other operations can be performed on the table for
    the duration of the backfill. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Create the new column, nullable.
    2. Set the default value of the new column to the volatile default.
    3. Backfill the new column for all existing rows.
    4. Create a check constraint: **CHECK (column IS NOT NULL) NOT VALID**.
    5. Validate the constraint.
    6. Set the column as NOT NULL.
    7. Drop the constraint.
    """

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and node.constraints:
            is_not_null = False
            has_static_default = False

            for constraint in node.constraints:
                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True

                if constraint.contype == enums.ConstrType.CONSTR_DEFAULT and isinstance(
                    constraint.raw_expr,
                    ast.A_Const,
                ):
                    has_static_default = True

            if is_not_null and not has_static_default:
                self.violations.add(
                    linter.Violation(
                        rule=self.code,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description="Not null constraint on new column with volatile default",  # noqa: E501
                        auto_fixable=self.is_auto_fixable,
                        help="Split the operation into multiple steps",
                    ),
                )
