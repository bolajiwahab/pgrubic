"""Checker for varchar."""

from pglast import ast, visitors

from pgshield.core import linter


class Varchar(linter.Checker):
    """## **What it does**
    Checks for usage of varchar.

    ## **Why not?**
    varchar(n) is a variable width text field that will throw an error if you try and
    insert a string longer than n characters (not bytes) into it.

    varchar (without the (n)) or text are similar, but without the length limit.
    If you insert the same string into the three field types they will take up exactly
    the same amount of space, and you won't be able to measure any difference
    in performance.

    If what you really need is a text field with an length limit then varchar(n) is
    great, but if you pick an arbitrary length and choose varchar(20) for a surname
    field you are risking production errors in the future when Hubert Blaine
    Wolfe­schlegel­stein­hausen­berger­dorff signs up for your service.

    Some databases do not have a type that can hold arbitrary long text, or if they do
    it's not as convenient or efficient or well-supported as varchar(n).
    Users from those databases will often use something like varchar(255) when what
    they really want is text.

    If you need to constrain the value in a field you probably need something more
    specific than a maximum length - maybe a minimum length too, or a limited set of
    characters - and a check constraint can do all of those things as well as a maximum
    string length.

    ## **When should you?**
    When you want to, really. If what you want is a text field that will throw an error
    if you insert too long a string into it, and you don't want to use an explicit check
    constraint then varchar(n) is a perfectly good type. Just don't use it automatically
    without thinking about it.

    Also, the varchar type is in the SQL standard, unlike the text type, so it might be
    the best choice for writing super-portable applications.

    ## **Use instead:**
    1. text
    2. text with a constraint that enforces a maximum string length
    """
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "varchar":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer text to varchar",
                ),
            )

            if self.is_fix_applicable:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "text",
                        },
                    ),
                )
