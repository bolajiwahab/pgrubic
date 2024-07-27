"""Checker for objects that are schema-qualifiable but are not schema qualified
at creation time.
"""

from pglast import ast

from pgshield.core import linter


class SchemaUnqualifiedObject(linter.Checker):
    """## **What it does**
    Checks for objects that are schema-qualifiable but are not schema qualified
    at creation time.

    ## **Why not?**
    Explicitly specifying schema improves code readability and improves clarity.

    ## **When should you?**
    If you really want to not specify schema.

    ## **Use instead:**
    Specify schema.
    """

    name: str = "schema.schema_qualification"
    code: str = "SCM001"

    description: str = "Database object should be schema qualified"

    is_auto_fixable: bool = False

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        if (
            isinstance(
                abs(ancestors).node,
                ast.CreateStmt
                | ast.CreateSeqStmt
                | ast.CreateEnumStmt
                | ast.IntoClause
                | ast.ViewStmt,
            )
            and not node.schemaname
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=self.description,
                ),
            )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        schema_name: str = node.typeName[0].sval if len(node.typeName) > 1 else None

        if not schema_name:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=self.description,
                ),
            )

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        schema_name: str = node.funcname[0].sval if len(node.funcname) > 1 else None

        if not schema_name:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=self.description,
                ),
            )
