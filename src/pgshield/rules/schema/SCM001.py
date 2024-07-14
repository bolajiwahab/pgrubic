"""Checker for objects that are schema-qualifiable but are not schema qualified."""

from pgshield.core import linter
from pgshield.rules.schema import Schema


class SchemaUnqualifiedObject(Schema):
    """## **What it does**
    Checks for objects that are schema-qualifiable but are not schema qualified.

    ## **Why not?**
    Explicitly specifying schema improves code readability and improves clarity.

    ## **When should you?**
    If you really want to not specify schema.

    ## **Use instead:**
    Specify schema.
    """

    name: str = "schema.schema_qualification"
    code: str = "SCM001"

    is_auto_fixable: bool = False

    def _check_schema(
        self,
        schema_name: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check that object is schema qualified."""
        if not schema_name:

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description="Database object should be schema qualified",
                ),
            )
