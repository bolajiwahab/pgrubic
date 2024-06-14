"""Naming."""

import re

from pglast import ast, enums  # type: ignore[import-untyped]

from pgshield.core import linter


class IndexNaming(linter.Checker):
    """Index naming."""

    name = "convention.index_naming"
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
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Index '{node.idxname}' does not follow naming"
                                f" convention '{self.config.regex_index}'",
                ),
            )


class ConstraintNaming(linter.Checker):
    """Constraint naming."""

    name = "convention.constraint_naming"
    code = "CVN002"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        constraint = {
            enums.ConstrType.CONSTR_PRIMARY: {
                "type": "Primary key",
                "naming_convention": self.config.regex_constraint_primary_key,
            },
            enums.ConstrType.CONSTR_FOREIGN: {
                "type": "Foreign key",
                "naming_convention": self.config.regex_constraint_foreign_key,
            },
            enums.ConstrType.CONSTR_UNIQUE: {
                "type": "Unique",
                "naming_convention": self.config.regex_constraint_unique_key,
            },
            enums.ConstrType.CONSTR_CHECK: {
                "type": "Check",
                "naming_convention": self.config.regex_constraint_check,
            },
            enums.ConstrType.CONSTR_EXCLUSION: {
                "type": "Ecxlusion",
                "naming_convention": self.config.regex_constraint_exclusion,
            },
        }

        if constraint.get(node.contype) and node.conname and (
            not re.match(constraint[node.contype]["naming_convention"], node.conname)
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"{constraint[node.contype]["type"]} constraint"
                                f" '{node.conname}' does not follow naming convention"
                                f" '{constraint[node.contype]["naming_convention"]}",
                ),
            )


class PartionNaming(linter.Checker):
    """Partition naming."""

    name = "convention.partition_naming"
    code = "CVN003"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit PartitionCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.partbound is not None
            and not re.match(self.config.regex_partition, node.relation.relname)
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Partition '{node.relation.relname}' does not follow"
                                f" naming convention '{self.config.regex_partition}'",
                ),
            )


class SequenceNaming(linter.Checker):
    """Sequence naming."""

    name = "convention.sequence_naming"
    code = "CVN004"

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not re.match(self.config.regex_sequence, node.sequence.relname)
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Sequence '{node.sequence.relname}' does not follow"
                                f" naming convention '{self.config.regex_sequence}'",
                ),
            )


class ConstraintShouldBeNamed(linter.Checker):
    """Constraint should be named."""

    name = "convention.constraint_should_be_named"
    code = "CVN005"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if not node.conname and node.contype != enums.ConstrType.CONSTR_NOTNULL:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Constraint should be named",
                ),
            )
