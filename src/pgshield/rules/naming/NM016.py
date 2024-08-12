"""Checker for date columns without suffix `_date`."""

from pglast import ast

from pgshield.core import linter


class DateColumnWithoutSuffix(linter.Checker):
    """## **What it does**
    Checks that date columns are suffixed with `_date`.

    ## **Why not?**
    Adding `_date` to a date column name makes it clear that the value represents the
    date when something happened. For example, `created_date` indicates the date when a
    record was created, and `updated_date` indicates the date when a record was last
    updated.

    Date columns could easily be confused with other types of data if not clearly
    named. For example, a column named created might be unclear — does it represent a
    boolean flag, a date, or something else? `created_date` removes this ambiguity by
    specifying that it's a date.

    ## **When should you?**
    Almost Never.

    ## **Use instead:**
    Add `_date` suffix to the date column name.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            node.typeName.names[-1].sval == "date"
            and node.colname
            and not node.colname.endswith("_date")
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Date column name should be suffixed with '_date'",
                ),
            )

            if self.can_apply_fix:

                node.colname += "_date"
