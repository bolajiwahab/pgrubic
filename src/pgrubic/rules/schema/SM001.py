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

            if (
                node.removeType
                in (
                    enums.ObjectType.OBJECT_TABLE,
                    enums.ObjectType.OBJECT_VIEW,
                    enums.ObjectType.OBJECT_MATVIEW,
                    enums.ObjectType.OBJECT_FOREIGN_TABLE,
                    enums.ObjectType.OBJECT_SEQUENCE,
                    enums.ObjectType.OBJECT_INDEX,
                )
                and len(obj) < SCHEMA_QUALIFIED_LENGTH
            ):

                self.violations.add(
                    linter.Violation(
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        source_text=self.source_text,
                        statement_location=self.statement_location,
                        description=f"Database object `{obj[0].sval}`"
                        " should be schema qualified",
                    ),
                )

            if (
                node.removeType == enums.ObjectType.OBJECT_TYPE
                and len(obj.names) < SCHEMA_QUALIFIED_LENGTH
            ):

                self.violations.add(
                    linter.Violation(
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        source_text=self.source_text,
                        statement_location=self.statement_location,
                        description=f"Database object `{obj.names[0].sval}`"
                        " should be schema qualified",
                    ),
                )

            if (
                node.removeType
                in (enums.ObjectType.OBJECT_FUNCTION, enums.ObjectType.OBJECT_PROCEDURE)
                and len(obj.objname) < SCHEMA_QUALIFIED_LENGTH
            ):

                self.violations.add(
                    linter.Violation(
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        source_text=self.source_text,
                        statement_location=self.statement_location,
                        description=f"Database object `{obj.objname[0].sval}`"
                        " should be schema qualified",
                    ),
                )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
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

    def visit_AlterEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterEnumStmt,
    ) -> None:
        """Visit AlterEnumStmt."""
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

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if len(node.funcname) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.funcname[0].svall}`"
                    " should be schema qualified",
                ),
            )

    def visit_AlterFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterFunctionStmt,
    ) -> None:
        """Visit AlterFunctionStmt."""
        if len(node.func.objname) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.func.objname[0].sval}`"
                    " should be schema qualified",
                ),
            )
