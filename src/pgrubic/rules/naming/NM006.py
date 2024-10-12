"""Checker for invalid exclusion constraint name according to naming convention."""

import re

from pglast import ast, enums, visitors

from pgrubic.core import linter


class InvalidExclusionConstraintName(linter.BaseChecker):
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

    ## **Configuration**
    `regex-constraint-exclusion`: Regex matching the naming convention for exclusion
    constraints.
    """

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_EXCLUSION
            and node.conname
            and (not re.match(self.config.lint.regex_constraint_exclusion, node.conname))
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description=f"Exclusion constraint"
                    f" `{node.conname}` does not follow naming convention"
                    f" `{self.config.lint.regex_constraint_exclusion}`",
                ),
            )
