"""Checker for invalid index name according to naming convention."""

import re

from pglast import ast

from pgshield.core import linter


class InvalidIndexName(linter.Checker):
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
    """

    name: str = "naming.invalid_index_name"
    code: str = "NM001"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if (
            not re.match(self.config.regex_index, node.idxname)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Index '{node.idxname}' does not follow naming"
                                f" convention '{self.config.regex_index}'",
                ),
            )
