"""Checker for new column with volatile default."""

import typing

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NewColumnWithVolatileDefault(linter.BaseChecker):
    """## **What it does**
    Checks new column with volatile default.

    ## **Why not?**
    Adding a new column with a volatile default to an already populated table will have
    to backfill the newly added column with the default, causing the table to be locked
    and rewritten, in which no other operations can be performed on the table for
    the duration of the rewrite. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Create the new column, nullable and without the volatile default.
    2. Set the default value for the newly created column.
    3. Backfill the newly created column for all existing rows.
    """

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and node.constraints:
            has_volatile_default = False

            for constraint in typing.cast(tuple[ast.Constraint], node.constraints):
                if (
                    constraint.contype == enums.ConstrType.CONSTR_DEFAULT
                    and not isinstance(
                        constraint.raw_expr,
                        ast.A_Const,
                    )
                ):
                    has_volatile_default = True

            if has_volatile_default:
                self.violations.add(
                    linter.Violation(
                        rule_code=self.code,
                        rule_name=self.name,
                        rule_category=self.category,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description="New column with volatile default",
                        is_auto_fixable=self.is_auto_fixable,
                        is_fix_enabled=self.is_fix_enabled,
                        help="Split the operation into multiple steps",
                    ),
                )
