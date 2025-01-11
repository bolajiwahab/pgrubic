"""Checker for objects that are schema-qualifiable but are not schema qualified."""

from pglast import ast, visitors

from pgrubic.core import linter

SCHEMA_QUALIFIED_LENGTH = 2


class SchemaUnqualifiedObject(linter.BaseChecker):
    """## **What it does**
    Checks for objects that are schema-qualifiable but are not schema qualified.

    We currently do not check **subqueries**.

    ## **Why not?**
    Explicitly specifying schema improves code readability and improves clarity.

    ## **When should you?**
    If you really do not want to specify schema.

    ## **Use instead:**
    Specify schema.
    """

    help: str = "Schema qualify the object"

    def _check_enum_for_schema(
        self,
        node: ast.CreateEnumStmt | ast.AlterEnumStmt,
    ) -> None:
        """Check enum for schema."""
        if len(node.typeName) < SCHEMA_QUALIFIED_LENGTH:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.typeName[0].sval}`"
                    " should be schema qualified",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help=self.help,
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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{function_name[0].sval}`"
                    " should be schema qualified",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help=self.help,
                ),
            )

    def visit_RangeVar(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        # Since CTEs are not schema qualifiable, they need to be excluded
        ctenames = []

        # we exclude referenced CTE names in CTEs
        if ancestors.find_nearest(ast.WithClause):
            ctenames = [
                cte.ctename for cte in ancestors.find_nearest(ast.WithClause).node.ctes
            ]

        # we exclude referenced CTE names in outer queries
        if (
            ancestors.find_nearest(
                ast.SelectStmt
                | ast.UpdateStmt
                | ast.DeleteStmt
                | ast.InsertStmt
                | ast.MergeStmt,
            )
            and ancestors.find_nearest(
                ast.SelectStmt
                | ast.UpdateStmt
                | ast.DeleteStmt
                | ast.InsertStmt
                | ast.MergeStmt,
            ).node.withClause
        ):
            ctenames = [
                cte.ctename
                for cte in ancestors.find_nearest(
                    ast.SelectStmt
                    | ast.UpdateStmt
                    | ast.DeleteStmt
                    | ast.InsertStmt
                    | ast.MergeStmt,
                ).node.withClause.ctes
            ]

        if (
            # there is no simple way to figure out if a subquery is referencing a CTE name
            # hence we are excluding all subqueries
            not (ancestors.find_nearest(ast.RangeSubselect | ast.SubLink))
            and node.relname not in ctenames
            and not node.schemaname
        ):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.relname}`"
                    " should be schema qualified",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help=self.help,
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
                        rule_code=self.code,
                        rule_name=self.name,
                        rule_category=self.category,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description=f"Database object `{object_names[-1].sval}`"
                        " should be schema qualified",
                        is_auto_fixable=self.is_auto_fixable,
                        is_fix_enabled=self.is_fix_enabled,
                        help=self.help,
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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Database object `{node.objname[0].sval}`"
                    " should be schema qualified",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help=self.help,
                ),
            )
