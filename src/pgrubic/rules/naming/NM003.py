"""Checker for invalid unique key constraint name according to naming convention."""

import re

from pglast import ast, enums, visitors

from pgrubic.core import linter


class InvalidUniqueKeyName(linter.BaseChecker):
    """## **What it does**
    Checks that the name of the unique key constraint to be created is valid according to
    naming convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your unique key constraint according to the set name convention.

    ## **Configuration**
    `regex-constraint-unique-key`: Regex matching the naming convention for unique key
    constraints.
    """

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_UNIQUE
            and node.conname
            and (not re.match(self.config.lint.regex_constraint_unique_key, node.conname))
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description=f"Unique key constraint"
                    f" `{node.conname}` does not follow naming convention"
                    f" `{self.config.lint.regex_constraint_unique_key}`",
                ),
            )
