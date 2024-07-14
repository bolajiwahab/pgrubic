"""Checker for usage of disallowed schemas."""

from pgshield.core import linter
from pgshield.rules.schema import Schema


class DisallowedSchema(Schema):
    """## **What it does**
    Checks for usage of disallowed schemas.

    ## **Why not?**
    If a schema has been included in the disallowed_schemas config, it is not allowed.

    ## **When should you?**
    Do you really want to use a disallowed schema?

    ## **Use instead:**
    Allowed schemas.
    """

    name: str = "schema.disallowed_schema"
    code: str = "SCM002"

    is_auto_fixable: bool = False

    def _check_schema(
        self,
        schema_name: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check schema is not disallowed."""
        if (
            schema_name
            and self.config.disallowed_schemas
        ):

            for schema in self.config.disallowed_schemas:

                if schema_name == schema.name:

                    self.violations.append(
                        linter.Violation(
                            statement_location=statement_location,
                            statement_length=statement_length,
                            node_location=node_location,
                            description=f"Schema '{schema_name}' is disallowed in config"
                            f""" in config with reason: '{schema.reason}'""",
                        ),
                    )
