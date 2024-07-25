"""Checker for char."""

from pglast import ast

from pgshield.core import linter


class Char(linter.Checker):
    r"""## **What it does**
    Checks for usage of char.

    ## **Why not?**
    Any string you insert into a char(n) field will be padded with spaces to the
    declared width. That's probably not what you actually want.

    The manual says:

    > Values of type character are physically padded with spaces to the specified
    > width n, and are stored and displayed that way.
    > However, trailing spaces are treated as semantically insignificant and disregarded
    > when comparing two values of type character. In collations where whitespace is
    > significant, this behavior can produce unexpected results; for example
    > SELECT 'a '::CHAR(2) collate "C" < E'a\n'::CHAR(2) returns true, even though
    > C locale would consider a space to be greater than a newline.
    > Trailing spaces are removed when converting a character value to one of the
    > other string types. Note that trailing spaces are semantically significant in
    > character varying and text values, and when using pattern matching, that is LIKE
    > and regular expressions. That should scare you off it.

    The space-padding does waste space, but doesn't make operations on it any faster;
    in fact the reverse, thanks to the need to strip spaces in many contexts.

    It's important to note that from a storage point of view char(n) is not a
    fixed-width type. The actual number of bytes varies since characters may take more
    than one byte, and the stored values are therefore treated as variable-length anyway
    (even though the space padding is included in the storage).

    Sometimes people respond to "don't use char(n)" with "but my values must always be
    exactly N characters long" (e.g. country codes, hashes, or identifiers from some
    other system). It is still a bad idea to use char(n) even in these cases.

    Remember, there is no performance benefit whatsoever to using char(n).
    In fact the reverse is true. One particular problem that comes up is that if you try
    and compare a char(n) field against a parameter where the driver has explicitly
    specified a type of text or varchar, you may be unexpectedly unable to use an index
    for the comparison. This can be hard to debug since it doesn't show up on
    manual queries.

    ## **When should you?**
    When you're porting very, very old software that uses fixed width fields. Or when
    you read the snippet from the manual above and think "yes, that makes perfect sense
    and is a good match for my requirements" rather than gibbering and running away.

    ## **Use instead:**
    1. text
    2. text with a constraint that enforces a maximum string length
    """

    name: str = "typing.char"
    code: str = "TYP005"

    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval in ["bpchar", "char"]:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer text over char",
                ),
            )

            if self.config.fix is True:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "text",
                        },
                    ),
                )
