"""Checker for security definer functions without explicit search path."""

from pgrubic.core import linter


class SecurityDefinerFunctionWithoutSearchPath(linter.BaseChecker):
    """## **What it does**
    Checks that a security definer function to be created has an explicit search path.

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
