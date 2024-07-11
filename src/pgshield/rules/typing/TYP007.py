"""Checker for money."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Money(linter.Checker):
    """## **What it does**
    Checks for usage of money.

    ## **Why not?**
    It's a fixed-point type, implemented as a machine int, so arithmetic with it is fast.
    But it doesn't handle fractions of a cent (or equivalents in other currencies), it's
    rounding behaviour is probably not what you want.

    It doesn't store a currency with the value, rather assuming that all money columns
    contain the currency specified by the database's lc_monetary locale setting. If you
    change the lc_monetary setting for any reason, all money columns will contain the
    wrong value. That means that if you insert '$10.00' while lc_monetary is set to
    'en_US.UTF-8' the value you retrieve may be '10,00 Lei' or '¥1,000' if lc_monetary
    is changed.

    Storing a value as a numeric, possibly with the currency being used in an adjacent
    column, might be better.

    ## **When should you?**
    If you're only working in a single currency, aren't dealing with fractional cents
    and are only doing addition and subtraction then money might be the right thing.

    ## **Use instead:**
    numeric
    """

    name: str = "convention.prefer_numeric_over_money"
    code: str = "TYP007"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (node.typeName.names[-1].sval == "money"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer numeric over money",
                ),
            )