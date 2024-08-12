"""Checker for cascade update."""

from pglast import ast, enums

from pgshield.core import linter


class CascadeUpdate(linter.Checker):
    """## **What it does**
    Checks for usage of cascade update.

    ## **Why not?**
    In theory primary key should be static so changes that need cascading should not
    need to happen. If you find yourself needing this sort of cascaded updates then that
    is perhaps a "code smell" in your database design.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Restrict
    """
    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_FOREIGN
            and node.fk_upd_action == enums.FKCONSTR_ACTION_CASCADE
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Found cascade update in foreign key constraint",
                ),
            )

            if self.can_apply_fix:
                node.fk_upd_action = enums.FKCONSTR_ACTION_RESTRICT
