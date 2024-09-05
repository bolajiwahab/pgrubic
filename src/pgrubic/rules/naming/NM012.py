"""Checker for identifiers with special characters."""

from pgrubic.core import linter
from pgrubic.rules.naming import CheckIdentifier


class SpecialCharacterInIdentifier(CheckIdentifier):
    """## **What it does**
    Checks for identifiers with special characters.

    ## **Why not?**
    SQL identifiers must begin with a letter (a-z) or an underscore (_). Subsequent
    characters in a name can be letters, digits (0-9), or underscores.

    PostgreSQL won't allow special characters in identifiers without double quotes.
    This means that if you use special characters in identifiers, you have to
    always double quote them. That is annoying enough by hand and error-prone.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove special characters from the identifier.
    """

    is_auto_fixable: bool = False

    def _check_identifier(
        self,
        identifier: str,
        line_number: int,
        column_offset: int,
        source_text: str,
        statement_location: int,
    ) -> None:
        """Checks for identifiers with special characters."""
        if identifier and not identifier.replace("_", "").isalnum():

            self.violations.add(
                linter.Violation(
                    line_number=line_number,
                    column_offset=column_offset,
                    source_text=source_text,
                    statement_location=statement_location,
                    description=f"Identifier should not contain Special characters '{identifier}'",  # noqa: E501
                ),
            )