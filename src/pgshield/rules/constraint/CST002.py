"""Checker for cascade delete."""

from pglast import ast, enums

from pgshield.core import linter


class CascadeDelete(linter.Checker):
    """## **What it does**
    Checks for usage of cascade update.

    ## **Why not?**
    Database schema should follow the principle of least surprise which
    says that every component in a system should behave in a way that most users
    expect it to behave, and therefore not surprise or astonish them.

    Cascading deletes should not cause unexpected loss of data. It is certainly
    dangerous if deleting a single table row can wipe out half your database.

    Are you certain you want to take the chance that someone will delete a single
    reference entry, unaware that doing so may delete a billion related transactions?

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
            and node.fk_del_action == enums.FKCONSTR_ACTION_CASCADE
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Found cascade delete in foreign key constraint",
                ),
            )

            if self.can_apply_fix:
                node.fk_del_action = enums.FKCONSTR_ACTION_RESTRICT
