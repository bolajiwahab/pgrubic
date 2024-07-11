"""Checker for xml."""
from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Xml(linter.Checker):
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

    name: str = "convention.prefer_jsonb_over_xml"
    code: str = "TYP013"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (node.typeName.names[-1].sval == "xml"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over xml",
                ),
            )