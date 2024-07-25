"""Checker for keywords used as identifiers."""

from pglast import keywords

from pgshield.core import linter
from pgshield.rules.naming import CollectIdentifiers


class KeywordIdentifier(CollectIdentifiers):
    """## **What it does**
    Checks for keywords used as identifiers.

    ## **Why not?**
    According to the standard, reserved key words are the only real key words; they are
    never allowed as identifiers. Non-reserved key words only have a special meaning in
    particular contexts and can be used as identifiers in other contexts.

    PostgreSQL won't allow reserved keywords as identifiers without double quotes.
    This means that if you use reserved keywords as identifiers, you have to always double
    quote them. That is annoying enough by hand and error-prone.

    Eventhough, non-reserved keywords can be used as identifiers in certain contexts,
    it can be confusing and ambiguious. Also, there is nothing stopping non-reserved
    keywords from becoming reserved keywords in the future. So, it is best to avoid them
    altogether.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Choose a name that is not a keyword.
    """

    name: str = "naming.keyword_identifier"
    code: str = "NM011"
    is_auto_fixable: bool = False

    def _check_identifier(
        self,
        identifier: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check for keywords used as identifiers."""
        full_keywords: set[str] = (
            set(keywords.RESERVED_KEYWORDS)
            .union(
                set(keywords.UNRESERVED_KEYWORDS),
            )
            .union(keywords.COL_NAME_KEYWORDS)
            .union(keywords.TYPE_FUNC_NAME_KEYWORDS)
        )

        if identifier in (full_keywords):

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Identifier '{identifier}' should not use keyword",
                ),
            )
