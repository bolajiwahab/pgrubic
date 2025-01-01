"""Checker for constant generated columns."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ConstantGeneratedColumn(linter.BaseChecker):
    """## **What it does**
    Checks for usage of constant generated columns.

    ## **Why not?**
    Always generating a constant value for a column is not useful and only leads to
    duplicated data all over the place and wastage of storage.

    ## **When should you?**
    If the table will be storing just one row at any point in time.

    ## **Use instead:**
    Generated column with expression.
    """

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_GENERATED and isinstance(
            node.raw_expr,
            ast.A_Const,
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
                    description=f"Generated column"
                    f" `{ancestors.find_nearest(ast.ColumnDef).node.colname}`"
                    " should not be a constant",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use an expression for the generated column",
                ),
            )
