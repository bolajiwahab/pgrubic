"""Checker for disallowed data types."""

from pglast import ast, visitors

from pgshield.core import linter


class DisallowedDataType(linter.BaseChecker):
    """## **What it does**
    Checks for usage of disallowed data types.

    ## **Why not?**
    If you are using a disallowed type, you're probably doing something wrong.

    ## **When should you?**
    Never. If a data type is intended to be used, it should not be in the blacklist.

    ## **Use instead:**
    Data types that are not in the blacklist.
    """
    is_auto_fixable: bool = True

    def visit_TypeName(
        self,
        ancestors: visitors.Ancestor,
        node: ast.TypeName,
    ) -> None:
        """Visit TypeName."""
        for data_type in self.config.disallowed_data_types:

            if node.names[-1].sval == data_type.name:

                self.violations.add(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Data type '{node.names[-1].sval}' is disallowed"
                        f" in config with reason: '{data_type.reason}', use"
                        f" '{data_type.use_instead}' instead",
                    ),
                )

                if self.is_fix_applicable:

                    node.names = (
                        {
                            "@": "String",
                            "sval": data_type.use_instead,
                        },
                    )
