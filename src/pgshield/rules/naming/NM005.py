"""Checker for invalid check constraint name according to naming convention."""
import re

from pglast import ast, enums

from pgshield.core import linter


class InvalidCheckConstraintName(linter.Checker):
    """## **What it does**
    Checks that the name of the check constraint to be created is valid according to
    naming convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your check constraint according to the set name convention.
    """

    name: str = "naming.invalid_check_constraint_name"
    code: str = "NM005"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_CHECK and node.conname and (
            not re.match(self.config.regex_constraint_check, node.conname)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Check constraint"
                                f" '{node.conname}' does not follow naming convention"
                                f" '{self.config.regex_constraint_check}'",
                ),
            )
