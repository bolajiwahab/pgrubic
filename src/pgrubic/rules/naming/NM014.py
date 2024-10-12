"""Checker for single letter identifiers."""

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

    def _check_identifier(
        self,
        identifier: str,
        line_number: int,
        column_offset: int,
        statement: str,
        statement_location: int,
    ) -> None:
        """Checks for identifiers prefix with pg_."""
        if identifier and len(identifier) == 1:
            self.violations.add(
                linter.Violation(
                    line_number=line_number,
                    column_offset=column_offset,
                    statement=statement,
                    statement_location=statement_location,
                    description=f"Single letter identifier `{identifier}`"
                    " is not descriptive enough",
                ),
            )
