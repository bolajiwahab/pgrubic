"""Checker for numeric with precision."""

from pglast import ast, visitors

from pgrubic.core import linter


class NumericWithPrecision(linter.BaseChecker):
    """## **What it does**
    Checks for usage of numeric with precision.

    ## **Why not?**
    Because it rounds off the fractional part which can lead to rounding errors slipping
    in when performing calculations and storing partial results before aggregation.
    An example of what could go wrong is
    [how-to-prevent-postgresql-from-automatically-rounding-numeric-types](https://dba.stackexchange.com/questions/281953/how-to-prevent-postgresql-from-automatically-rounding-numeric-types){:target="_blank"}

    ## **When should you?**
    When you want to, really. If what you want is a numeric field that will throw an
    error when you insert too large a value into it, and you do not want to use an
    explicit check constraint and you always want to store the fractional part in a
    specific decimal places then numeric(p, s) is a perfectly good type.
    Just don't use it automatically without thinking about it.

    ## **Use instead:**
    numeric.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "numeric" and node.typeName.typmods:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Prefer entire numeric",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use numeric",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.typeName = ast.TypeName(
            names=(
                {
                    "@": "String",
                    "sval": "numeric",
                },
            ),
        )
