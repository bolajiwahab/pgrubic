"""Checker for json."""

from pglast import ast, visitors

from pgshield.core import linter


class Json(linter.Checker):
    """## **What it does**
    Checks for usage of json.

    ## **Why not?**
    From the manual:
    > The json and jsonb data types accept almost identical sets of values as input.
    > The major practical difference is one of efficiency. The json data type stores an
    > exact copy of the input text, which processing functions must reparse on each
    > execution; while jsonb data is stored in a decomposed binary format that makes it
    > slightly slower to input due to added conversion overhead, but significantly
    > faster to process, since no reparsing is needed. jsonb also supports indexing,
    > which can be a significant advantage.

    ## **When should you?**
    In general, most applications should prefer to store JSON data as jsonb, unless
    there are quite specialized needs, such as legacy assumptions about ordering of
    object keys.

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
        if node.typeName.names[-1].sval == "json":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over json",
                ),
            )

            if self.is_fix_applicable:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "jsonb",
                        },
                    ),
                )
