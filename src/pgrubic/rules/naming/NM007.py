"""Checker for invalid sequence name according to naming convention."""

import re

from pglast import ast, visitors

from pgrubic.core import linter


class InvalidSequenceName(linter.BaseChecker):
    """## **What it does**
    Checks that the name of the sequence to be created is valid according to naming
    convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your sequence according to the set name convention.

    ## **Configuration**
    `regex-sequence`: Regex matching the naming convention for sequences.
    """

    is_auto_fixable: bool = False

    def visit_CreateSeqStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        if not re.match(self.config.lint.regex_sequence, node.sequence.relname):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Sequence `{node.sequence.relname}` does not follow"
                    f" naming convention `{self.config.lint.regex_sequence}`",
                ),
            )
