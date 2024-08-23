"""Checker for column data type change."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class ColumnDataTypeChange(linter.BaseChecker):
    """## **What it does**
    Checks for column data type change.

    ## **Why not?**
    Changing a column's data type requires an **ACCESS EXCLUSIVE** lock on the table,
    preventing both reads and writes. Generally, such change forces a rewrite of the
    whole table and indexes with every other transactions being blocked for
    the duration of the rewrite.
    As an exception to rewrite, when changing the type of an existing column, if the USING
    clause does not change the column contents and the old type is either binary coercible
    to the new type or an unconstrained domain over the new type, a table rewrite is not
    needed. However, indexes must always be rebuilt unless the system can verify that the
    new index would be logically equivalent to the existing one.

    This change might also cause errors and break applications that rely on the
    column potentially disrupting business operations.

    ## **When should you?**
    If the above exception to table and index rewrite is applicable and the clients have
    been made aware of the new type.

    ## **Use instead:**
    1. Create a new column with the new type.
    2. Start writing data to the new column.
    3. Copy all data from the old column to the new column.
    4. Migrate clients to the new column.
    5. Drop the old column.
    """
    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_AlterColumnType:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid column data type change",
                ),
            )
