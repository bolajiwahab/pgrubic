"""Checker for duplicate index column."""

from pglast import ast, visitors

from pgrubic.core import linter


class DuplicateIndexColumn(linter.BaseChecker):
    """## **What it does**
    Checks for duplicate index column.

    ## **Why not?**
    Having duplicate column in an index is redundant and unnecessary.
    Indexes are not free, they add an overhead to write operations,
    and having a column repeated does not add any benefit but rather unnecessary
    index maintenance and storage.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove duplicate column from the index.
    """

    is_auto_fixable: bool = True

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        columns: list[str] = [column.name for column in node.indexParams if column.name]
        duplicate_columns = {column for column in columns if columns.count(column) > 1}

        for column in duplicate_columns:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Column `{column}` specified more than once in index",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help=f"Remove duplicate column `{column}` from index",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.IndexStmt) -> None:
        """Fix violation."""
        index_params: list[ast.IndexElem] = []

        for param in node.indexParams:
            if param.name not in [column.name for column in index_params]:
                index_params.append(param)

        node.indexParams = index_params
