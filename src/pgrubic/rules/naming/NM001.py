"""Checker for invalid index name according to naming convention."""

import re

from pglast import ast, visitors

from pgrubic.core import linter


class InvalidIndexName(linter.BaseChecker):
    """## **What it does**
    Checks that the name of the index to be created is valid according to naming
    convention.

    ## **Why not?**
    Naming conventions are crucial in database design as they offer consistency, clarity,
    and structure to the organization and accessibility of data within a database.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Name your index according to the set name convention.

    ## **Configuration**
    `regex-index`: Regex matching the naming convention for indexes.
    """

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if node.idxname and not re.match(self.config.lint.regex_index, node.idxname):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Index `{node.idxname}` does not follow naming"
                    f" convention `{self.config.lint.regex_index}`",
                ),
            )
