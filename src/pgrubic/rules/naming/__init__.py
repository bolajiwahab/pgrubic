"""Rules for naming."""

import abc

from pglast import ast, visitors

from pgrubic.core import linter


class CheckIdentifier(abc.ABC, linter.BaseChecker):
    """Check identifier."""

    @abc.abstractmethod
    def _check_identifier(
        self,
        *,
        identifier: str,
        line_number: int,
        column_offset: int,
        statement: str,
        statement_location: int,
    ) -> None:
        """Check identifier for violations."""

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        self._check_identifier(
            identifier=node.relation.relname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        self._check_identifier(
            identifier=node.colname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_ViewStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        self._check_identifier(
            identifier=node.view.relname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        self._check_identifier(
            identifier=node.idxname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        self._check_identifier(
            identifier=node.sequence.relname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateSchemaStmt,
    ) -> None:
        """Visit CreateSchemaStmt."""
        self._check_identifier(
            identifier=node.schemaname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        self._check_identifier(
            identifier=node.funcname[-1].sval,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
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
                statement=self.statement,
                statement_location=self.statement_location,
            )

    def visit_CreatedbStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
        self._check_identifier(
            identifier=node.dbname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateRoleStmt,
    ) -> None:
        """Visit CreateRoleStmt."""
        self._check_identifier(
            identifier=node.role,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateTableSpaceStmt,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        self._check_identifier(
            identifier=node.tablespacename,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateTrigStmt,
    ) -> None:
        """Visit CreateTrigStmt."""
        self._check_identifier(
            identifier=node.trigname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CreateEnumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        self._check_identifier(
            identifier=node.typeName[-1].sval,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_RuleStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        self._check_identifier(
            identifier=node.rulename,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_IntoClause(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IntoClause,
    ) -> None:
        """Visit IntoClause."""
        self._check_identifier(
            identifier=node.rel.relname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )

    def visit_CompositeTypeStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CompositeTypeStmt,
    ) -> None:
        """Visit IntoClause."""
        self._check_identifier(
            identifier=node.typevar.relname,
            line_number=self.line_number,
            column_offset=self.column_offset,
            statement=self.statement,
            statement_location=self.statement_location,
        )
