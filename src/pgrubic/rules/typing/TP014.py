"""Checker for disallowed data types."""

from pglast import ast, visitors

from pgrubic.core import config, linter


class DisallowedDataType(linter.BaseChecker):
    """## **What it does**
    Checks for usage of disallowed data types.

    ## **Why not?**
    If you are using a disallowed type, you're probably doing something wrong.

    ## **When should you?**
    Never. If a data type is intended to be used, it should not be in the
    disallowed_data_types.

    ## **Use instead:**
    Data types that are not in the disallowed_data_types.

    ## **Configuration**
    `disallowed_data_types`: List of disallowed data types.
    """

    is_auto_fixable: bool = True

    def visit_TypeName(
        self,
        ancestors: visitors.Ancestor,
        node: ast.TypeName,
    ) -> None:
        """Visit TypeName."""
        for data_type in self.config.lint.disallowed_data_types:
            if node.names[-1].sval == data_type.name:
                self.violations.add(
                    linter.Violation(
                        rule_code=self.code,
                        rule_name=self.name,
                        rule_category=self.category,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description=f"Data type '{node.names[-1].sval}' is disallowed"
                        f" in config with reason: '{data_type.reason}', use"
                        f" '{data_type.use_instead}' instead",
                        auto_fixable=self.is_auto_fixable,
                        help=f"Use '{data_type.use_instead}' instead",
                    ),
                )

                self._fix(node, data_type)

    def _fix(self, node: ast.TypeName, data_type: config.DisallowedDataType) -> None:
        """Fix violation."""
        node.names = (
            {
                "@": "String",
                "sval": data_type.use_instead,
            },
        )
