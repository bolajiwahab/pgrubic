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
        line: str,
        statement_location: int,
    ) -> None:
        """Checks for identifiers with single letter."""
        if identifier and len(identifier.strip()) == 1:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=line_number,
                    column_offset=column_offset,
                    line=line,
                    statement_location=statement_location,
                    description=f"Single letter identifier `{identifier}`"
                    " is not descriptive enough",
                ),
            )
