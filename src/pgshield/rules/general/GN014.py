"""Checker for existence of not null constraint on required columns."""

from pglast import ast, enums, stream

from pgshield.core import linter


class NullableRequiredColumn(linter.Checker):
    """## **What it does**
    Checks for existence of not null constraint on required columns.

    ## **Why not?**
    If a column has been specified as required then it should not be nullable.
    Having a required column as nullable is an anti-pattern and should be avoided.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Set the required column as **Not Null**.
    """

    name: str = "general.remove_not_null_from_required_column"
    code: str = "GN014"

    is_auto_fixable: bool = False

    def _register_violation(
        self,
        column_name: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.append(
            linter.Violation(
                statement_location=statement_location,
                statement_length=statement_length,
                node_location=node_location,
                description=f"Column '{column_name}' is marked as required"
                            " in config",
            ),
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        # if ast.CreateStmt in ancestors and node.colname in self.config.not_null_columns:
        for column in self.config.required_columns:

            if node.colname == column.name:
                print(column.name)

                is_not_null = bool(
                    (
                        [
                            constraint
                            for constraint in node.constraints
                            if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                        ]
                        if node.constraints is not None
                        else []
                    ),
                )

                print(is_not_null, node.colname)

                if not is_not_null:

                    self._register_violation(
                        column_name=node.colname,
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                    )

                    if self.config.fix is True:

                        node.constraints = (
                            *(node.constraints or []),
                            ast.Constraint(
                                contype=enums.ConstrType.CONSTR_NOTNULL,
                            ),
                        )

        print(stream.RawStream()(node))
    # def visit_AlterTableCmd(
    #     self,
    #     ancestors: ast.Node,
    #     node: ast.AlterTableCmd,
    # ) -> None:
    #     """Visit AlterTableCmd."""
    #     if (
    #         node.subtype == enums.AlterTableType.AT_DropNotNull
    #         and node.name in self.config.not_null_columns
    #     ):

    #         self._register_violation(
    #             column_name=node.name,
    #             statement_location=self.statement_location,
    #             statement_length=self.statement_length,
    #             node_location=self.node_location,
    #         )

    # def visit_AlterTableCmd(
    #         self,
    #         ancestors: ast.Node,
    #         node: ast.AlterTableCmd,
    #     ) -> None:
    #         """Visit AlterTableCmd."""
    #         if (
    #             node.subtype == enums.AlterTableType.AT_DropNotNull
    #         ):

    #             for column in self.config.required_columns:

    #                 if node.name == column.name:

    #                     self.violations.append(
    #                         linter.Violation(
    #                             statement_location=self.statement_location,
    #                             statement_length=self.statement_length,
    #                             node_location=self.node_location,
    #                             description=f"Column {node.name} is marked as required"
    #                             " in config",
    #                         ),
    #                     )
