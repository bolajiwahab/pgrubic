"""Checker for objects that are schema-qualifiable but are not schema qualified."""

from pglast import ast, enums

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

    is_auto_fixable: bool = False

    def _check_enum_for_schema(
        self,
        node: ast.CreateEnumStmt | ast.AlterEnumStmt,
    ) -> None:
        """Check enum for schema."""
        if len(node.typeName) < SCHEMA_QUALIFIED_LENGTH:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
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
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Database object `{function_name[0].sval}`"
                    " should be schema qualified",
                ),
            )

    def _check_to_be_dropped_object_for_schema(
        self,
        object_name: tuple[ast.String, ...],
    ) -> None:
        """Check to-be-dropped object for schema."""
        if len(object_name) < SCHEMA_QUALIFIED_LENGTH:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Database object `{object_name[0].sval}`"
                    " should be schema qualified",
                ),
            )

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

            if node.removeType in (
                enums.ObjectType.OBJECT_TABLE,
                enums.ObjectType.OBJECT_VIEW,
                enums.ObjectType.OBJECT_MATVIEW,
                enums.ObjectType.OBJECT_FOREIGN_TABLE,
                enums.ObjectType.OBJECT_SEQUENCE,
                enums.ObjectType.OBJECT_INDEX,
            ):

                self._check_to_be_dropped_object_for_schema(obj)

            if node.removeType == enums.ObjectType.OBJECT_TYPE:

                self._check_to_be_dropped_object_for_schema(obj.names)

            if (
                node.removeType
                in (enums.ObjectType.OBJECT_FUNCTION, enums.ObjectType.OBJECT_PROCEDURE)
                and len(obj.objname) < SCHEMA_QUALIFIED_LENGTH
            ):

                self._check_to_be_dropped_object_for_schema(obj.objname)

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
