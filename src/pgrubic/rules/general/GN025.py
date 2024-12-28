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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Duplicate index detected",
                    auto_fixable=self.is_auto_fixable,
                    help="Remove duplicate indexes",
                ),
            )

        self.seen_indexes.append(index_definition)
