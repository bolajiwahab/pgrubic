"""Naming."""

import re

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import recover_original_identifier
from pgshield.core import linter


class IndexNaming(linter.Checker):  # type: ignore[misc]
    """Index naming."""

    name = "unsafe.index_naming"
    code = "CVN001"

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not re.match(self.config.regex_index, node.idxname)
            and (
                ancestors[statement_index].stmt_location,
                self.code,
            )
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description=f"Index '{node.idxname}' does not follow naming convention '{self.config.regex_index}'",  # noqa: E501
                ),
            )


class CheckConstraintNaming(linter.Checker):  # type: ignore[misc]
    """Check constraint naming."""

    name = "unsafe.check_constraint_naming"
    code = "CVN002"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not re.match(self.config.regex_constraint_check, node.conname)
            and (
                ancestors[statement_index].stmt_location,
                self.code,
            )
            not in self.ignore_rules
        ):
            
            print(enums.ConstrType.CONSTR_PRIMARY == node.contype)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description=f"{enums.ConstrType(node.contype).name} constraint '{node.conname}' does not follow naming convention '{self.config.regex_constraint_check}'",  # noqa: E501
                ),
            )
