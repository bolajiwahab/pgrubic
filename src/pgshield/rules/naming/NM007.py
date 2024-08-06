"""Checker for invalid sequence name according to naming convention."""

import re

from pglast import ast

from pgshield.core import linter


class InvalidSequenceName(linter.Checker):
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
    """
    is_auto_fixable: bool = False

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        if not re.match(self.config.regex_sequence, node.sequence.relname):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Sequence '{node.sequence.relname}' does not follow"
                    f" naming convention '{self.config.regex_sequence}'",
                ),
            )
