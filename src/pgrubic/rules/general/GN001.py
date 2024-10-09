"""Checker for table inheritance."""

from pglast import ast, visitors

from pgrubic.core import linter


class TableInheritance(linter.BaseChecker):
    """## **What it does**
    Checks for usage of table inheritance.

    ## **Why not?**
    Table inheritance was a part of a fad wherein the database was closely coupled to
    object-oriented code. It turned out that coupling things that closely didn't
    actually produce the desired results.

    ## **When should you?**
    Never …almost. Now that table partitioning is done natively, that common use case
    for table inheritance has been replaced by a native feature that handles tuple
    routing, etc., without bespoke code. One of the very few exceptions would be
    temporal_tables extension if you are in a pinch and want to use that for row
    versioning in place of a lacking SQL 2011 support. Table inheritance will provide a
    small shortcut instead of using UNION ALL to get both historical as well as current
    rows. Even then you ought to be wary of caveats while working with parent table.

    ## **Use instead:**
    Don't use table inheritance. If you think you want to, use foreign keys instead.
    """

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.inhRelations and not node.partbound:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Table inheritance detected",
                ),
            )
