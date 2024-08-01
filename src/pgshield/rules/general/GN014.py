"""Checker for usage of select into to create a new table."""

from pglast import ast

from pgshield.core import linter


class SelectInto(linter.Checker):
    """## **What it does**
    Checks for usage of select into to create a new table.

    ## **Why not?**
    The SQL standard uses SELECT INTO to represent selecting values into scalar
    variables of a host program, rather than creating a new table.

    The PostgreSQL usage of SELECT INTO to represent table creation is historical.
    Some other SQL implementations also use SELECT INTO in this way (but most SQL
    implementations support CREATE TABLE AS instead). Apart from such compatibility
    considerations, it is best to use CREATE TABLE AS for this purpose in new code.

    ## **When should you?**
    Never.

    ## **Use instead:**
    CREATE TABLE AS.
    """
    is_auto_fixable: bool = False

    def visit_IntoClause(
        self,
        ancestors: ast.Node,
        node: ast.IntoClause,
    ) -> None:
        """Visit IntoClause."""
        if not isinstance(
            abs(ancestors).node,
            ast.CreateTableAsStmt,
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Use CREATE TABLE AS instead of SELECT INTO",
                ),
            )
