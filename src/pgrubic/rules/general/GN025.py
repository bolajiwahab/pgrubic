"""Checker for duplicate indexes."""

from pglast import ast, visitors

from pgrubic.core import config, linter


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

    def __init__(self, *, config: config.Config) -> None:
        """Initialize the DuplicateIndex checker."""
        super().__init__(config=config)
        self.seen_indexes: list[tuple[object, object, object, object]] = []

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
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Remove duplicate indexes",
                ),
            )

        self.seen_indexes.append(index_definition)
