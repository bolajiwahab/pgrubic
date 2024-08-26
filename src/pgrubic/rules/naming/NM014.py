"""Checker for ID column."""

from pgrubic.core import linter
from pgrubic.rules.naming import CheckIdentifier


class SingleLetterIdentifier(CheckIdentifier):
    """## **What it does**
    Checks for usage of single letter identifiers.

    ## **Why not?**
    Single letter identifier does not provide much information about what the identifier
    represents. Using a more descriptive name can improve clarity, readability, and
    maintainability of the database schema.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Descriptive name.
    """

    is_auto_fixable: bool = False

    def _check_identifier(
        self,
        identifier: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Checks for identifiers prefix with pg_."""
        if identifier and len(identifier) == 1:

            self.violations.add(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Single letter identifier found: '{identifier}'",
                ),
            )
