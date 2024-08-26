"""Checker for identifiers prefix with pg_."""

from pgrubic.core import linter
from pgrubic.rules.naming import CheckIdentifier


class PgPrefixIdentifier(CheckIdentifier):
    """## **What it does**
    Checks for identifiers prefix with pg_.

    ## **Why not?**
    From the documentation:

    Schema names beginning with pg_ are reserved for system purposes and cannot be
    created by users.

    Since system table names begin with pg_, it is best to avoid such names to ensure that
    you won't suffer a conflict if some future version defines a system table named the
    same as your table. (With the default search path, an unqualified reference to your
    table name would then be resolved as the system table instead.)
    System tables will continue to follow the convention of having names beginning with
    pg_, so that they will not conflict with unqualified user-table names so long as users
    avoid the pg_ prefix.

    Same thing applies to other objects such as functions, views, sequences etc.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove prefix pg_ from identifier.
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
        if identifier and identifier.startswith("pg_"):

            self.violations.add(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description="Identifier should not use prefix 'pg_'",
                ),
            )
