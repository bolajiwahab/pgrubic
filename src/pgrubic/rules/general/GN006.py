"""Checker for creation of enum."""

from pglast import ast, visitors

from pgrubic.core import linter


class CreateEnum(linter.BaseChecker):
    """## **What it does**
    Checks for creation of enum.

    ## **Why not?**
    Enum types are primarily intended for static sets of values, though there is support
    for adding new values to an existing enum type, and for renaming values however
    existing values cannot be removed from an enum type, nor can the sort ordering of
    such values be changed, short of dropping and re-creating the enum type.

    ## **When should you?**
    If your set of values are fixed such that you won't be removing values
    in the future. Just don't use it automatically without thinking about it.

    ## **Use instead:**
    Mapping table.
    """

    def visit_CreateEnumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        self.violations.add(
            linter.Violation(
                rule_code=self.code,
                rule_name=self.name,
                rule_category=self.category,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Prefer mapping table to enum",
                auto_fixable=self.is_auto_fixable,
                help="Use mapping table",
            ),
        )
