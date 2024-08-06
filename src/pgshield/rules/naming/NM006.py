"""Checker for invalid exclusion constraint name according to naming convention."""

import re

from pglast import ast, enums

from pgshield.core import linter


class InvalidExclusionConstraintName(linter.Checker):
    """## **What it does**
    Checks that the name of the exclusion constraint to be created is valid.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your exclusion constraint according to the set name convention.
    """
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_EXCLUSION
            and node.conname
            and (not re.match(self.config.regex_constraint_exclusion, node.conname))
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Exclusion constraint"
                    f" '{node.conname}' does not follow naming convention"
                    f" '{self.config.regex_constraint_exclusion}'",
                ),
            )
