"""Checker for invalid foreign key constraint name according to naming convention."""

import re

from pglast import ast, enums, visitors

from pgshield.core import linter


class InvalidForeignKeyName(linter.BaseChecker):
    """## **What it does**
    Checks that the name of the foreign key constraint to be created is valid according to
    naming convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your foreign key constraint according to the set name convention.
    """
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_FOREIGN
            and node.conname
            and (not re.match(self.config.regex_constraint_foreign_key, node.conname))
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Foreign key constraint"
                    f" '{node.conname}' does not follow naming convention"
                    f" '{self.config.regex_constraint_foreign_key}'",
                ),
            )
