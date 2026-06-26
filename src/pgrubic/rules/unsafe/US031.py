"""Checker for new column with volatile default."""

from pglast import ast, enums, visitors

from pgrubic import is_non_volatile_function
from pgrubic.core import linter


class NewColumnWithVolatileDefault(linter.BaseChecker):
    """## **What it does**
    Checks new column with volatile default.

    ## **Why not?**
    Adding a new column with a volatile default to an already populated table will have
    to backfill the newly added column with the default, causing the table to be locked,
    in which no other operations can be performed on the table for the duration of the
    backfill. This will cause downtime if the table is concurrently being accessed by
    other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Note**
    Unqualified references to known non-volatile built-in functions are assumed to resolve
    to pg_catalog. Shadowing built-in functions via search_path is not modeled and may
    lead to missed diagnostics.

    ## **Use instead:**
    1. Create the new column, nullable.
    2. Set the default value for the newly created column.
    3. Backfill the newly created column for all existing rows.
    """

    def visit_FuncCall(
        self,
        ancestors: visitors.Ancestor,
        node: ast.FuncCall,
    ) -> None:
        """Visit FuncCall."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and ancestors.find_nearest(ast.ColumnDef)
            and ancestors.find_nearest(ast.Constraint)
            and ancestors.find_nearest(ast.Constraint).node.contype
            == enums.ConstrType.CONSTR_DEFAULT
            and not is_non_volatile_function(function=node)
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
                    description="New column with a volatile default",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Split the operation into multiple steps",
                ),
            )
