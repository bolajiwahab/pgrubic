"""Checker for xml."""

from pglast import ast, visitors

from pgrubic.core import linter


class Xml(linter.BaseChecker):
    """## **What it does**
    Checks for usage of xml.

    ## **Why not?**
    Downsides to using XML include slower processing and querying due to its complexity,
    higher storage requirements and challenges in efficient indexing, rigidity in
    adapting to schema changes, and the overall complexity in data handling due to XML's
    verbose and hierarchical structure. These factors suggest that XML can lead to
    increased resource usage and development difficulties, making formats like JSON more
    suitable.

    ## **When should you?**
    Despite its drawbacks, XML might be suitable when there is a need for data
    interchange with systems that require XML format, or when dealing with legacy
    systems where data is already in XML format.

    ## **Use instead:**
    jsonb.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "xml":

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Prefer jsonb over xml",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.typeName = ast.TypeName(
            names=(
                {
                    "@": "String",
                    "sval": "jsonb",
                },
            ),
        )
