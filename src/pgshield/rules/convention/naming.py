"""Naming."""

import re

from pglast import ast, enums

from pgshield.core import linter


class IndexNaming(linter.Checker):
    """Index naming."""

    name: str = "convention.index_naming"
    code: str = "CVN001"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if (
            not re.match(self.config.regex_index, node.idxname)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Index '{node.idxname}' does not follow naming"
                                f" convention '{self.config.regex_index}'",
                ),
            )


class ConstraintNaming(linter.Checker):
    """Constraint naming."""

    name: str = "convention.constraint_naming"
    code: str = "CVN002"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
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
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"{constraint[node.contype]["type"]} constraint"
                                f" '{node.conname}' does not follow naming convention"
                                f" '{constraint[node.contype]["naming_convention"]}",
                ),
            )


class PartionNaming(linter.Checker):
    """Partition naming."""

    name: str = "convention.partition_naming"
    code: str = "CVN003"

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit PartitionCmd."""
        if (
            node.partbound is not None
            and not re.match(self.config.regex_partition, node.relation.relname)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Partition '{node.relation.relname}' does not follow"
                                f" naming convention '{self.config.regex_partition}'",
                ),
            )


class SequenceNaming(linter.Checker):
    """Sequence naming."""

    name: str = "convention.sequence_naming"
    code: str = "CVN004"

    is_auto_fixable: bool = False

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        if (
            not re.match(self.config.regex_sequence, node.sequence.relname)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Sequence '{node.sequence.relname}' does not follow"
                                f" naming convention '{self.config.regex_sequence}'",
                ),
            )


class PreferNamedConstraint(linter.Checker):
    """Prefer named constraint."""

    name: str = "convention.prefer_named_constraint"
    code: str = "CVN005"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if not node.conname and node.contype in (
            enums.ConstrType.CONSTR_CHECK,
            enums.ConstrType.CONSTR_PRIMARY,
            enums.ConstrType.CONSTR_UNIQUE,
            enums.ConstrType.CONSTR_EXCLUSION,
            enums.ConstrType.CONSTR_FOREIGN,
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer named constraint",
                ),
            )
