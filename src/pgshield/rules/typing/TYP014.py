"""Checker for hstore."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Hstore(linter.Checker):
    """## **What it does**
    Checks for usage of hstore.

    ## **Why not?**
    Hstore is essentially a key/value store directly in Postgres. With hstore you are a
    little more limited in terms of the datatypes you have: you essentially just get
    strings. You also don't get any nesting; in short it's a flat key/value datatype.

    ## **When should you?**
    Hstore can work fine for text based key-value lookups, but in general JSONB can
    still work great here.

    ## **Use instead:**
    jsonb.
    """

    name: str = "typing.prefer_jsonb_over_hstore"
    code: str = "TYP014"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "hstore"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over hstore",
                ),
            )
