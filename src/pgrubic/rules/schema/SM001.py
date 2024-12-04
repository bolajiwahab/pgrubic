"""Checker for objects that are schema-qualifiable but are not schema qualified."""

from pglast import ast

from pgrubic.core import linter

SCHEMA_QUALIFIED_LENGTH = 2


class SchemaUnqualifiedObject(linter.BaseChecker):
    """## **What it does**
    Checks for objects that are schema-qualifiable but are not schema qualified.

    ## **Why not?**
    Explicitly specifying schema improves code readability and improves clarity.

    ## **When should you?**
    If you really want to not specify schema.

    ## **Use instead:**
    Specify schema.
    """

    def _check_enum_for_schema(
        self,
        node: ast.CreateEnumStmt | ast.AlterEnumStmt,
    ) -> None:
        """Check enum for schema."""
        if len(node.typeName) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.typeName[0].sval}`"
                    " should be schema qualified",
                ),
            )

    def _check_function_for_schema(
        self,
        function_name: tuple[ast.String, ...],
    ) -> None:
        """Check function for schema."""
        if len(function_name) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{function_name[0].sval}`"
                    " should be schema qualified",
                ),
            )

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        # We exclude DML lines here due to the possibility of
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
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.relname}`"
                    " should be schema qualified",
                ),
            )

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        for obj in node.objects:
            object_names = getattr(obj, "names", getattr(obj, "objname", obj))

            if (
                isinstance(object_names, tuple | list)
                and len(object_names) < SCHEMA_QUALIFIED_LENGTH
            ):
                self.violations.add(
                    linter.Violation(
                        rule=self.code,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description=f"Database object `{object_names[-1].sval}`"
                        " should be schema qualified",
                    ),
                )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        self._check_enum_for_schema(node)

    def visit_AlterEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterEnumStmt,
    ) -> None:
        """Visit AlterEnumStmt."""
        self._check_enum_for_schema(node)

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        self._check_function_for_schema(node.funcname)

    def visit_AlterFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterFunctionStmt,
    ) -> None:
        """Visit AlterFunctionStmt."""
        self._check_function_for_schema(node.func.objname)

    def visit_ObjectWithArgs(
        self,
        ancestors: ast.Node,
        node: ast.ObjectWithArgs,
    ) -> None:
        """Visit ObjectWithArgs."""
        if len(node.objname) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.objname[0].sval}`"
                    " should be schema qualified",
                ),
            )
