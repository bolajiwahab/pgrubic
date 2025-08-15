"""Checker for security definer functions without explicit search path."""

import typing

from pglast import ast, enums as pglast_enums, visitors

from pgrubic.core import enums, linter


class SecurityDefinerFunctionNoExplicitSearchPath(linter.BaseChecker):
    """## **What it does**
    Checks that a security definer function has explicit search path.

    ## **Why not?**
    Because a **SECURITY DEFINER** function is executed with the privileges of the user
    that owns it, care is needed to ensure that the function cannot be misused.
    For security, **search_path** should be set to exclude any schemas writable by
    untrusted users. This prevents malicious users from creating objects (e.g., tables,
    functions, and operators) that mask objects intended to be used by the function.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Set an explicit **search_path** on SECURITY DEFINER functions.
    """

    is_auto_fixable = True

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit a CreateFunctionStmt."""
        is_security_definer = False
        has_explicit_search_path = False

        for option in typing.cast(tuple[ast.DefElem], node.options):
            name = option.defname

            if name == enums.FunctionOption.SECURITY and option.arg.boolval:
                is_security_definer = True

            if (
                name == enums.FunctionOption.SET
                and isinstance(option.arg, ast.VariableSetStmt)
                and option.arg.kind == pglast_enums.VariableSetKind.VAR_SET_VALUE
                and option.arg.name == "search_path"
            ):
                has_explicit_search_path = True

        if is_security_definer and not has_explicit_search_path:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Security definer function with no explicit search path",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Set explicit search_path on security definer functions",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.CreateFunctionStmt) -> None:
        """Fix violation."""
        options_without_search_path = tuple(
            option
            for option in typing.cast(tuple[ast.DefElem], node.options)
            if not (
                option.defname == enums.FunctionOption.SET
                and option.arg.name == "search_path"
            )
        )

        node.options = (
            *options_without_search_path,
            ast.DefElem(
                defname="set",
                arg=ast.VariableSetStmt(
                    kind=pglast_enums.VariableSetKind.VAR_SET_VALUE,
                    name="search_path",
                    args=(
                        ast.A_Const(isnull=False, val=ast.String(sval="")),
                        ast.A_Const(isnull=False, val=ast.String(sval="pg_temp")),
                    ),
                ),
            ),
        )
