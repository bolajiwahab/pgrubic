"""Checker for duplicate column in primary key constraint."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class DuplicatePrimaryKeyColumn(linter.BaseChecker):
    """## **What it does**
    Checks for duplicate column in primary key.

    ## **Why not?**
    While PostgreSQL does not allow duplicate columns in a primary key constraint,
    such constructs are still parseable, but will error out at runtime.

    Having a duplicate column in a primary key is an obvious error.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove duplicate column from the primary key constraint.
    """

    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_PRIMARY:
            columns: list[str] = [key.sval for key in node.keys or []]
            duplicate_columns = {
                column for column in columns if columns.count(column) > 1
            }

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
                        description=f"Column `{column}` specified more than once in primary key constraint",  # noqa: E501
                        is_auto_fixable=self.is_auto_fixable,
                        is_fix_enabled=self.is_fix_enabled,
                        help="Remove duplicate column from primary key constraint",
                    ),
                )

            self._fix(node)

    def _fix(self, node: ast.Constraint) -> None:
        """Fix violation."""
        keys: list[ast.IndexElem] = []

        for key in node.keys:
            if key.sval not in [column.sval for column in keys]:
                keys.append(key)

        node.keys = keys
