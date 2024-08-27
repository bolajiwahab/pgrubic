"""Checker for invalid partition name according to naming convention."""

import re

from pglast import ast, visitors

from pgrubic.core import linter


class InvalidPartitionName(linter.BaseChecker):
    """## **What it does**
    Checks that the name of the partition to be created is valid according to naming
    convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your partition according to the set name convention.
    """

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.partbound is not None and not re.match(
            self.config.lint.regex_partition,
            node.relation.relname,
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Partition '{node.relation.relname}' does not follow"
                    f" naming convention '{self.config.lint.regex_partition}'",
                ),
            )
