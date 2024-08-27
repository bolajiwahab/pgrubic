"""Checker for missing primary key."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class MissingPrimaryKey(linter.BaseChecker):
    """## **What it does**
    Checks for existence of primary keys.

    ## **Why not?**
    A primary key is a set of attributes which prevents duplicates and can uniquely
    identify a record.

    If you don't have one, you cannot tell records apart and you
    create a burden for yourself by checking for duplicate records.

    ## **When should you?**
    Never for OLTP databases.

    If you are doing analytics (OLAP) at scale, then primary
    keys may not be very useful.

    ## **Use instead:**
    Define a primary key.
    """

    is_auto_fixable: bool = False

    def _check_for_table_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for table level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.Constraint)
                    and definition.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def _check_for_column_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for column level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.ColumnDef) and definition.constraints
                    for constraint in definition.constraints
                    if constraint.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if (
            node.tableElts
            and not self._check_for_column_level_primary_key(node)
            and not self._check_for_table_level_primary_key(node)
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Table '{node.relation.relname}' missing a primary key",
                ),
            )
