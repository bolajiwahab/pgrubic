"""Rules for naming."""

import abc
import typing

from pglast import ast, visitors

from pgrubic.core import linter


class ABCBaseCheckerMeta(abc.ABCMeta, linter.CheckerMeta):
    """Combine ABCMeta and CheckerMeta."""


class CheckIdentifier(abc.ABC, linter.BaseChecker, metaclass=ABCBaseCheckerMeta):
    """Check identifier."""

    @abc.abstractmethod
    def _check_identifier(
        self,
        *,
        identifier: str,
        line_number: int,
        column_offset: int,
        line: str,
        statement_location: int,
    ) -> None:
        """Check identifier for violations."""

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        relation = typing.cast(ast.RangeVar, node.relation)
        relation_name = typing.cast(str, relation.relname)
        self._check_identifier(
            identifier=relation_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.colname is None:
            return
        self._check_identifier(
            identifier=node.colname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_ViewStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        view = typing.cast(ast.RangeVar, node.view)
        view_name = typing.cast(str, view.relname)
        self._check_identifier(
            identifier=view_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        index_name = typing.cast(str, node.idxname)
        self._check_identifier(
            identifier=index_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        sequence = typing.cast(ast.RangeVar, node.sequence)
        sequence_name = typing.cast(str, sequence.relname)
        self._check_identifier(
            identifier=sequence_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateSchemaStmt,
    ) -> None:
        """Visit CreateSchemaStmt."""
        schema_name = typing.cast(str, node.schemaname)
        self._check_identifier(
            identifier=schema_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        function_name = typing.cast(tuple[ast.String, ...], node.funcname)
        self._check_identifier(
            identifier=typing.cast(str, function_name[-1].sval),
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.conname is not None:
            self._check_identifier(
                identifier=node.conname,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
            )

    def visit_CreatedbStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
        database_name = typing.cast(str, node.dbname)
        self._check_identifier(
            identifier=database_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateRoleStmt,
    ) -> None:
        """Visit CreateRoleStmt."""
        role_name = typing.cast(str, node.role)
        self._check_identifier(
            identifier=role_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateTableSpaceStmt,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        tablespace_name = typing.cast(str, node.tablespacename)
        self._check_identifier(
            identifier=tablespace_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateTrigStmt,
    ) -> None:
        """Visit CreateTrigStmt."""
        trigger_name = typing.cast(str, node.trigname)
        self._check_identifier(
            identifier=trigger_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CreateEnumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        type_name = typing.cast(tuple[ast.String, ...], node.typeName)
        self._check_identifier(
            identifier=typing.cast(str, type_name[-1].sval),
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_RuleStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        rule_name = typing.cast(str, node.rulename)
        self._check_identifier(
            identifier=rule_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_IntoClause(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IntoClause,
    ) -> None:
        """Visit IntoClause."""
        relation = typing.cast(ast.RangeVar, node.rel)
        relation_name = typing.cast(str, relation.relname)
        self._check_identifier(
            identifier=relation_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_CompositeTypeStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CompositeTypeStmt,
    ) -> None:
        """Visit IntoClause."""
        type_var = typing.cast(ast.RangeVar, node.typevar)
        type_name = typing.cast(str, type_var.relname)
        self._check_identifier(
            identifier=type_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )

    def visit_RenameStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        new_name = typing.cast(str, node.newname)
        self._check_identifier(
            identifier=new_name,
            line_number=self.line_number,
            column_offset=self.column_offset,
            line=self.line,
            statement_location=self.statement_location,
        )
