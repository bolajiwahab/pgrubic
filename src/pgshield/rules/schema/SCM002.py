"""Checker for usage of disallowed schemas."""

from pglast import ast

from pgshield.core import linter


class DisallowedSchema(linter.Checker):
    """## **What it does**
    Checks for usage of disallowed schemas.

    ## **Why not?**
    If a schema has been included in the disallowed_schemas config, it is not allowed.

    ## **When should you?**
    Do you really want to use a disallowed schema?

    ## **Use instead:**
    Allowed schemas.
    """
    is_auto_fixable: bool = True

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        if isinstance(
            abs(ancestors).node,
            ast.CreateStmt
            | ast.ViewStmt
            | ast.CompositeTypeStmt
            | ast.CreateSeqStmt
            | ast.IntoClause,
        ):

            for schema in self.config.disallowed_schemas:

                if node.schemaname == schema.name:

                    self.violations.append(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Schema '{node.schemaname}' is disallowed in"
                            f" config with reason: '{schema.reason}'"
                            f", use '{schema.use_instead}' instead",
                        ),
                    )

                    if self.config.fix is True:

                        node.schemaname = schema.use_instead

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        schema_name: str = node.typeName[0].sval if len(node.typeName) > 1 else None

        for schema in self.config.disallowed_schemas:

            if schema_name == schema.name:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Schema '{schema_name}' is disallowed in"
                        f" config with reason: '{schema.reason}'"
                        f", use '{schema.use_instead}' instead",
                    ),
                )

                if self.config.fix is True:

                    node.typeName[0].sval = schema.use_instead

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        schema_name: str = node.funcname[0].sval if len(node.funcname) > 1 else None

        for schema in self.config.disallowed_schemas:

            if schema_name == schema.name:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Schema '{schema_name}' is disallowed in"
                        f" config with reason: '{schema.reason}'"
                        f", use '{schema.use_instead}' instead",
                    ),
                )

                if self.config.fix is True:

                    node.funcname[0].sval = schema.use_instead
