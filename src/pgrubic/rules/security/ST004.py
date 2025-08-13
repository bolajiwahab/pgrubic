"""Checker for security definer functions without pg_temp as the last element in the
search path.
"""

import typing

from pglast import ast, visitors

from pgrubic.core import linter


class SecurityDefinerFunctionWithoutPgTempAsLastElementInSearchPath(linter.BaseChecker):
    """## **What it does**
    Checks that a security definer function has pg_temp as the last element in the search
    path.

    ## **Why not?**
    Because a **SECURITY DEFINER** function is executed with the privileges of the user
    that owns it, care is needed to ensure that the function cannot be misused.
    For security, **search_path** should be set to exclude any schemas writable by
    untrusted users. This prevents malicious users from creating objects (e.g., tables,
    functions, and operators) that mask objects intended to be used by the function.
    A secure arrangement can be obtained by forcing the temporary schema to be searched
    last.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Always include **pg_temp** as the last element in **search_path** on a SECURITY
    DEFINER function.
    """

    is_auto_fixable = True

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit a CreateFunctionStmt."""
        is_security_definer = False
        has_search_path = False
        last_element_in_search_path = None

        for option in typing.cast(tuple[ast.DefElem], node.options):
            name = option.defname.upper()
            if name == "SECURITY" and option.arg.boolval:
                is_security_definer = True
            elif name == "SET" and option.arg.name == "search_path":
                has_search_path = True
                last_element_in_search_path = option.arg.args[-1].val.sval

        if (
            is_security_definer
            and has_search_path
            and last_element_in_search_path != "pg_temp"
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
                    description="Security definer function without pg_temp as the last element in the search path",  # noqa: E501
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Set pg_temp as the last element in the search path",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.CreateFunctionStmt) -> None:
        """Fix violation."""
        for option in typing.cast(tuple[ast.DefElem], node.options):
            if option.defname.upper() == "SET" and option.arg.name == "search_path":
                non_temp_schemas = tuple(
                    schema
                    for schema in typing.cast(tuple[ast.A_Const], option.arg.args)
                    if schema.val.sval != "pg_temp"
                )
                option.arg.args = (*non_temp_schemas, ast.String(sval="pg_temp"))
