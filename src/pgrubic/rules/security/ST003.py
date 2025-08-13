"""Checker for security definer functions without search path."""

from pglast import ast, visitors

from pgrubic.core import linter


class SecurityDefinerFunctionWithoutSearchPath(linter.BaseChecker):
    """## **What it does**
    Checks that a security definer function has a search path.

    ## **Why not?**
    Because a **SECURITY DEFINER** function is executed with the privileges of the user
    that owns it, care is needed to ensure that the function cannot be misused.
    For security, **search_path** should be set to exclude any schemas writable by
    untrusted users. This prevents malicious users from creating objects (e.g., tables,
    functions, and operators) that mask objects intended to be used by the function.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Always set **search_path** on a SECURITY DEFINER function.
    """

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit a CreateFunctionStmt."""
        is_security_definer = False
        has_search_path = False

        for option in node.options:
            name = option.defname.upper()
            if name == "SECURITY" and option.arg.boolval:
                is_security_definer = True

            if name == "SET" and option.arg.name == "search_path":
                has_search_path = True

        if is_security_definer and not has_search_path:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Security definer function without search path",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Set search_path on security definer functions",
                ),
            )
