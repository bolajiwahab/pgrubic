"""Checker for hstore."""

from pglast import ast, visitors

from pgrubic.core import linter


class Hstore(linter.BaseChecker):
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

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "hstore":
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description="Prefer jsonb over hstore",
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
