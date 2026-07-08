"""Checker for self assigning column."""

from pglast import ast, visitors

from pgrubic.core import linter


class SelfAssigningColumn(linter.BaseChecker):
    """## **What it does**
    Checks for self assigning columns.

    ## **Why not?**
    Assigning a column to itself does not change its value but still causes PostgreSQL to
    process the row as an update, create a new row version, creating unnecessary write
    amplification, dead tuples, WAL, and potential table and index bloats.

    In most cases, this assignment is redundant or indicates that a different value was
    intended.

    ## **When should you?**
    Almost never. Intentional self-assignments are rare and are typically used only to
    force UPDATE semantics, such as firing triggers.

    ## **Use instead:**
    Use the correct value or remove the assignment entirely.
    """

    def _target_alias(self, update_statement: visitors.Ancestor) -> str:
        """Get the target alias of the update statement."""
        relation = update_statement.node.relation

        if relation.alias is not None:
            return str(relation.alias.aliasname)

        return str(relation.relname)

    def _is_self_assignment(
        self,
        update_statement: visitors.Ancestor,
        column: ast.ColumnRef,
    ) -> bool:
        """Check if the assignment is a self-assignment."""
        fields = [field.sval for field in column.fields]
        target_column = column.fields[-1].sval

        unqualified_column_length = 1
        table_qualified_column_length = 2
        schema_table_qualified_column_length = 3
        catalog_schema_table_qualified_column_length = 4

        # column
        if len(fields) == unqualified_column_length:
            return bool(fields[0] == target_column)

        # alias.column/table.column
        if len(fields) == table_qualified_column_length:
            relation, column = fields

            return bool(
                column == target_column
                and relation
                == self._target_alias(
                    update_statement,
                ),
            )

        # schema.table.column
        if len(fields) == schema_table_qualified_column_length:
            schema, table, column = fields
            relation = update_statement.node.relation

            return bool(
                column == target_column
                and schema == relation.schemaname
                and table == relation.relname,
            )

        # catalog.schema.table.column
        if len(fields) == catalog_schema_table_qualified_column_length:
            catalog, schema, table, column = fields

            relation = update_statement.node.relation

            return bool(
                column == target_column
                and catalog == relation.catalogname
                and schema == relation.schemaname
                and table == relation.relname,
            )

        return False

    def visit_ResTarget(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ResTarget,
    ) -> None:
        """Visit ResTarget."""
        update_stmt = ancestors.find_nearest(ast.UpdateStmt)

        if not update_stmt or not isinstance(node.val, ast.ColumnRef):
            return

        if self._is_self_assignment(update_stmt, node.val):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Self assigning column",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Avoid self-assignments in UPDATE statements",
                ),
            )
