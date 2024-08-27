"""Checker for usage of NOT IN."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NotIn(linter.BaseChecker):
    """## **What it does**
    Checks for indexed foreign keys.

    ## **Why not?**
    Don't use NOT IN, or any combination of NOT and IN such as NOT (x IN (select…))

    Two reasons:

    1. NOT IN behaves in unexpected ways if there is a null present:
    ```sql
    select * from foo where col not in (1,null); -- always returns 0 rows
    ```
    ```sql
    select * from foo where foo.col not in (select bar.x from bar); -- returns 0 rows if
    any value of bar.x is null
    ```

    This happens because col IN (1,null) returns TRUE if col=1, and NULL otherwise (i.e.
    it can never return FALSE). Since NOT (TRUE) is FALSE, but NOT (NULL) is still NULL,
    there is no way that NOT (col IN (1,null)) (which is the same thing as col NOT IN
    (1,null)) can return TRUE under any circumstances.

    2. Because of point 1 above, NOT IN (SELECT ...) does not optimize very well.
    In particular, the planner can't transform it into an anti-join, and so it becomes
    either a hashed Subplan or a plain Subplan. The hashed subplan is fast, but the
    planner only allows that plan for small result sets; the plain subplan is horrifically
    slow (in fact O(N²)). This means that the performance can look good in small-scale
    tests but then slow down by 5 or more orders of magnitude once a size threshold is
    crossed; you do not want this to happen.

    ## **When should you?**
    NOT IN (list,of,values,...) is mostly safe unless you might have a null in the list
    (via a parameter or otherwise). So it's sometimes natural and even advisable to use
    it when excluding specific constant values from a query result.

    ## **Use instead:**
    In most cases, the NULL behavior of NOT IN (SELECT …) is not intentionally desired,
    and the query can be rewritten using NOT EXISTS (SELECT …):
    ```sql
    select * from foo where not exists (select from bar where foo.col = bar.x);
    ```
    """

    is_auto_fixable: bool = False

    def visit_A_Expr(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Expr,
    ) -> None:
        """Visit A_Expr."""
        if node.kind == enums.A_Expr_Kind.AEXPR_IN and node.name[-1].sval == "<>":

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="NOT IN detected",
                ),
            )
