"""Checker for nullable boolean field."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class MismatchColumnInDataTypeChange(linter.Checker):
    """## **What it does**
    Checks for mismatch column in data type change.

    ## **Why not?**
    For certain column data type changes, a **USING** clause must be provided if there is
    no implicit or assignment cast from old to new type.
    Logically, the expression in the USING should reference the original column otherwise
    it is most likely a mistake.

    ## **When should you?**
    Almost never. When you are sure that the expression in the USING is indeed correct.

    ## **Use instead:**
    The right column in the USING clause.
    """

    is_auto_fixable: bool = True

    def visit_ColumnRef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnRef,
    ) -> None:
        """Visit ColumnRef."""
        alter_table_cmd: visitors.Ancestor = ancestors.find_nearest(ast.AlterTableCmd)

        if (
            alter_table_cmd
            and alter_table_cmd.node.subtype
            == enums.AlterTableType.AT_AlterColumnType
            and alter_table_cmd.node.name
            != node.fields[0].sval
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Column '{alter_table_cmd.node.name}' in data type"
                                f" change does not match column '{node.fields[0].sval}'"
                                " in USING clause",
                ),
            )
