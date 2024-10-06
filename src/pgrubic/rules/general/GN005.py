"""Checker for index elements."""

from pglast import ast, visitors

from pgrubic.core import linter


class IndexElementsMoreThanThree(linter.BaseChecker):
    """## **What it does**
    Checks for indexes with more than three elements.

    ## **Why not?**
    From the documentation:
    > Multicolumn indexes should be used sparingly. In most situations, an index on a
    > single column is sufficient and saves space and time.
    > Indexes with more than three columns are unlikely to be helpful unless the usage of
    > the table is extremely stylized.

    ## **When should you?**
    If you really need to.

    See https://www.postgresql.org/docs/current/indexes-bitmap-scans.html for some
    discussion of the merits of different index configurations.

    ## **Use instead:**
    Keep your index elements at most three.
    """

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        max_index_elements = 3

        if len(node.indexParams) > max_index_elements:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Index elements more than {max_index_elements}",
                ),
            )
