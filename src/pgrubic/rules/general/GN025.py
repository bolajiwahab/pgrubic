"""Checker for duplicate indexes."""

import typing

from pglast import ast, visitors

from pgrubic.core import linter


class DuplicateIndex(linter.BaseChecker):
    """## **What it does**
    Checks for duplicate indexes (exact match).

    ## **Why not?**
    Having duplicate indexes can negatively affect performance of database operations in
    several ways, some of which are as follows:

    - Slower Write Operations
    - Maintenance Overhead
    - Increased Storage Costs

    In summary, indexes are not cheap and what is worst is having them duplicated.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove the duplicate.
    """

    is_auto_fixable: bool = False

    seen_indexes: typing.ClassVar[list[typing.Any]] = []

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        index_definition = (
            node.relation,
            node.indexParams,
            node.indexIncludingParams,
            node.whereClause,
        )

        if index_definition in self.seen_indexes:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Duplicate index detected",
                ),
            )

        self.seen_indexes.append(index_definition)
