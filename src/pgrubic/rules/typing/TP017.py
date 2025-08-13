"""Checker for nullable boolean field."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NullableBooleanField(linter.BaseChecker):
    """## **What it does**
    Checks for nullable boolean field.

    ## **Why not?**
    3 possible values is not a boolean. By allowing nulls in a boolean field, you are
    turning an intended binary representation (true/false) into a ternary representation
    (true, false, null). Null is neither 'true' nor 'false'.
    Allowing nulls in a boolean field is an oversight that leads to unnecessarily
    ambiguous data.

    ## **When should you?**
    Never.

    ## **Use instead:**
    boolean with not null constraint.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "bool":
            is_not_null = bool(
                (
                    [
                        constraint
                        for constraint in node.constraints
                        if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                    ]
                    if node.constraints is not None
                    else []
                ),
            )

            if not is_not_null:
                self.violations.add(
                    linter.Violation(
                        rule_code=self.code,
                        rule_name=self.name,
                        rule_category=self.category,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description="Boolean field should not be nullable",
                        is_auto_fixable=self.is_fix_applicable,
                        is_fix_enabled=self.is_fix_enabled,
                        help="Add not null constraint",
                    ),
                )

                self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.constraints = (
            *(node.constraints or []),
            ast.Constraint(
                contype=enums.ConstrType.CONSTR_NOTNULL,
            ),
        )
