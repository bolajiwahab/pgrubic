"""Checker for timestamp without time zone."""

from pglast import ast, visitors

from pgrubic.core import linter


class TimestampWithoutTimezone(linter.BaseChecker):
    """## **What it does**
    Checks for usage of timestamp without time zone.

    ## **Why not?**
    timestamptz (also known as timestamp with time zone) zone records a single moment
    in time. Despite what the name says it doesn't store a timestamp, just a point
    in time described as the number of microseconds since January 1st, 2000 in UTC.
    You can insert values in any timezone and it'll store the point in time that value
    describes. By default it will display times in your current timezone, but you can
    use at time zone to display it in other time zones. Because it stores a point in
    time, it will do the right thing with arithmetic involving timestamps entered in
    different timezones - including between timestamps from the same location on
    different sides of a daylight savings time change.

    timestamp (also known as timestamp without time zone) doesn't do any of that,
    it just stores a date and time you give it. You can think of it being a picture of
    a calendar and a clock rather than a point in time.
    Without additional information - the timezone - you don't know what time it records.
    Because of that, arithmetic between timestamps from different locations or between
    timestamps from summer and winter may give the wrong answer.

    So if what you want to store is a point in time, rather than a picture of a clock,
    use timestamptz (timestamp with time zone).

    ## **When should you?**
    If you're dealing with timestamps in an abstract way, or just saving and retrieving
    them from an app, where you aren't going to be doing arithmetic with them then
    timestamp might be suitable.

    ## **Use instead:**
    timestamptz (also known as timestamp with time zone).
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "timestamp":

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Prefer timestamp with timezone over timestamp without timezone",  # noqa: E501
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.typeName = ast.TypeName(
            names=(
                {
                    "@": "String",
                    "sval": "timestamptz",
                },
            ),
        )
