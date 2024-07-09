"""Checker for char."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.convention.typing import is_column_creation


class Char(linter.Checker):
    r"""## **What it does**
    Checks for usage of char.

    ## **Why not?**
    Any string you insert into a char(n) field will be padded with spaces to the
    declared width. That's probably not what you actually want.

    The manual says:

        Values of type character are physically padded with spaces to the specified
        width n, and are stored and displayed that way. However, trailing spaces are
        treated as semantically insignificant and disregarded when comparing two
        values of type character. In collations where whitespace is significant,
        this behavior can produce unexpected results; for example
        SELECT 'a '::CHAR(2) collate "C" < E'a\n'::CHAR(2) returns true, even though
        C locale would consider a space to be greater than a newline.
        Trailing spaces are removed when converting a character value to one of the
        other string types. Note that trailing spaces are semantically significant in
        character varying and text values, and when using pattern matching, that is LIKE
        and regular expressions. That should scare you off it.

    The space-padding does waste space, but doesn't make operations on it any faster;
    in fact the reverse, thanks to the need to strip spaces in many contexts.

    It's important to note that from a storage point of view char(n) is not a
    fixed-width type. The actual number of bytes varies since characters may take more
    than one byte, and the stored values are therefore treated as variable-length anyway
    (even though the space padding is included in the storage).

    ## **When should you?**
    When you're porting very, very old software that uses fixed width fields. Or when
    you read the snippet from the manual above and think "yes, that makes perfect sense
    and is a good match for my requirements" rather than gibbering and running away.

    ## **Use instead:**
    text.
    """

    name: str = "convention.prefer_text_over_char"
    code: str = "TYP005"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (
            node.typeName.names[-1].sval in ["bpchar", "char"]
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer text over char",
                ),
            )
