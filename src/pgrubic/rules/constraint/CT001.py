"""Checker for cascade update."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class CascadeUpdate(linter.BaseChecker):
    """## **What it does**
    Checks for usage of cascade update.

    ## **Why not?**
    In theory primary key should be static so changes that need cascading should not
    need to happen. If you find yourself needing this sort of cascaded updates then that
    is perhaps a **code smell** in your database design.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Restrict
    """

    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_FOREIGN
            and node.fk_upd_action == enums.FKCONSTR_ACTION_CASCADE
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
                    description="Cascade update in foreign key constraint",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Handle the updates manually",
                ),
            )

            self._fix(ancestors=ancestors, node=node)

    def _fix(self, ancestors: visitors.Ancestor, node: ast.Constraint) -> None:
        """Fix violation."""
        node.fk_upd_action = enums.FKCONSTR_ACTION_RESTRICT
        if ancestors.find_nearest(ast.AlterTableCmd):
            node.skip_validation = True
