"""Checker for invalid check constraint name according to naming convention."""

import re

from pglast import ast, enums, visitors

from pgrubic.core import linter


class InvalidCheckConstraintName(linter.BaseChecker):
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

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_CHECK
            and node.conname
            and (not re.match(self.config.lint.regex_constraint_check, node.conname))
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Check constraint"
                    f" `{node.conname}` does not follow naming convention"
                    f" `{self.config.lint.regex_constraint_check}`",
                ),
            )
