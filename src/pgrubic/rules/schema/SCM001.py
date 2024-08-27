"""Checker for objects that are schema-qualifiable but are not schema qualified
at creation time.
"""

from pglast import ast

from pgrubic.core import linter


class SchemaUnqualifiedObject(linter.BaseChecker):
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

    description: str = "Database object should be schema qualified"

    is_auto_fixable: bool = False

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        # We exclude DML statements here due to the possibility of
        # Common Table Expressions which are not schema qualified
        if (
            not isinstance(
                abs(ancestors).node,
                ast.SelectStmt
                | ast.UpdateStmt
                | ast.InsertStmt
                | ast.DeleteStmt
                | ast.Query
                | ast.WithClause
                | ast.CommonTableExpr,
            )
            and not node.schemaname
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
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

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
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

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=self.description,
                ),
            )
