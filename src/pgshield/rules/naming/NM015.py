"""Checker for timestamp columns without suffix `_at`."""

from pglast import ast, visitors

from pgshield.core import linter


class TimestampColumnWithoutSuffix(linter.BaseChecker):
    """## **What it does**
    Checks that timestamp columns are suffixed with `_at`.

    ## **Why not?**
    Adding `_at` to a timestamp column name makes it clear that the value represents the
    time when something happened. For example, `created_at` indicates the time when a
    record was created, and `updated_at` indicates the time when a record was last
    updated.

    Timestamp columns could easily be confused with other types of data if not clearly
    named. For example, a column named created might be unclear — does it represent a
    boolean flag, a date, or something else? `created_at` removes this ambiguity by
    specifying that it's a timestamp.

    ## **When should you?**
    Almost Never.

    ## **Use instead:**
    Add `_at` suffix to the timestamp column name.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            node.typeName.names[-1].sval
            in [
                "timestamptz",
                "timestamp",
            ]
            and node.colname
            and node.colname
            not in [column.name for column in self.config.required_columns]
            and not node.colname.endswith("_at")
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Timestamp column name should be suffixed with '_at'",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.colname += "_at"
