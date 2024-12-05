"""Checker for removal of constraints."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class RemoveConstraint(linter.BaseChecker):
    """## **What it does**
    Checks for removal of constraints.

    ## **Why not?**
    Constraints are used to ensure data quality, data integrity, consistency,
    and adherence to certain business rules.

    If a constraint is removed without due consideration, the data in the database can
    become corrupted.

    ## **When should you?**
    You can remove constraints if they are no longer needed or need adjustment. Don't just
    remove them without due consideration.

    ## **Use instead:**
    **No suggestions**.
    """

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype in (
            enums.AlterTableType.AT_DropConstraint,
            enums.AlterTableType.AT_DropNotNull,
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Constraint `{node.name}` removal detected",
                    auto_fixable=self.is_auto_fixable,
                ),
            )
