"""Checker for typed table."""

from pglast import ast, visitors

from pgrubic.core import linter


class TypedTable(linter.BaseChecker):
    """## **What it does**
    Checks for typed table.

    ## **Why not?**
    A typed table takes its structure from a composite type.

    A typed table is tied to its type; for example the table will be dropped if the type
    is dropped (with DROP TYPE ... CASCADE).

    This creates a tight coupling between the table and its type. Any operations to be
    done to the columns of the typed table would have to be done through the type.

    ## **When should you?**
    Almost Never.

    ## **Use instead:**
    A template table, copying the structure with **LIKE**.
    """

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.ofTypename:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="A typed table is tightly coupled to its type",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use a template table, copying the structure with **LIKE**",
                ),
            )
