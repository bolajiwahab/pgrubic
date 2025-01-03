"""Checker for date columns without defined suffix, by default `_date`."""

from pglast import ast, visitors

from pgrubic.core import linter


class DateColumnWithoutSuffix(linter.BaseChecker):
    """## **What it does**
    Checks that date columns are suffixed with the defined suffix, by default `_date`.

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
    Add the defined suffix or the default `_date` to to the date column name.

    ## **Configuration**
    `date-column-suffix`: Specify the suffix for date columns.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            node.typeName.names[-1].sval == "date"
            and node.colname
            and not node.colname.endswith(self.config.lint.date_column_suffix)
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
                    description="Date column name should be suffixed with"
                    f" `{self.config.lint.date_column_suffix}`",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Add the set suffix to the date column",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.colname += self.config.lint.date_column_suffix
