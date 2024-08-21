"""Checker for serial types."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class Serial(linter.Checker):
    """## **What it does**
    Checks for usage of serial types.

    ## **Why not?**
    The serial types have some weird behaviors that make schema, dependency, and
    permission management unnecessarily cumbersome.

    ## **When should you?**
    - If you need support to PostgreSQL older than version 10.
    - In certain combinations with table inheritance (but see there)
    - More generally, if you somehow use the same sequence for multiple tables, although
      in those cases an explicit declaration might be preferable over the serial types.

    ## **Use instead:**
    For new applications, identity columns should be used.
    """

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        alter_table_cmd: visitors.Ancestor = ancestors.find_nearest(ast.AlterTableCmd)

        if (
            (
                alter_table_cmd
                and alter_table_cmd.node.subtype
                == enums.AlterTableType.AT_AddColumn
            )
            or ancestors.find_nearest(ast.CreateStmt)
            and node.typeName.names[-1].sval in ["smallserial", "serial", "bigserial"]
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer identity column over serial types",
                ),
            )

            if self.is_fix_applicable:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "bigint",
                        },
                    ),
                )

                node.constraints = (
                    *(node.constraints or []),
                    ast.Constraint(
                        contype=enums.ConstrType.CONSTR_IDENTITY,
                        generated_when=enums.ATTRIBUTE_IDENTITY_ALWAYS,
                    ),
                )
