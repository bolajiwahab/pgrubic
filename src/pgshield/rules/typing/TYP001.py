"""Checker for timestamp without time zone."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class TimestampWithoutTimezone(linter.Checker):
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

    name: str = (
        "convention.prefer_timestamp_with_timezone_over_timestamp_without_timezone"
    )
    groups: tuple[str, ...] = ("convention", "typing")
    code: str = "TYP001"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "timestamp"
            and node.typeName.names[0].sval == "pg_catalog"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer timestamp with timezone over timestamp without timezone",  # noqa: E501
                ),
            )

            if self.config.fix is True:

                node.typeName.names[-1].sval = "timestamptz"