"""Convention around identifiers."""

from pglast import ast, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class UpperCaseForIdentifier(linter.Checker):  # type: ignore[misc]
    """No upper case in identifier."""

    name = "convention.upper_case_in_identifier"
    code = "CVN022"

    def _check_identifier(self, identifier: str, location: int, statement: str) -> None:
        """Check for uppercase in identifier."""
        if any(ele.isupper() for ele in identifier):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description="Uppercase found in identifier",
                ),
            )

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.relation.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors:

            statement_index: int = utils.get_statement_index(ancestors)

            self._check_identifier(
                node.colname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_ViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ViewStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.view.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableAsStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTableAsStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.into.rel.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.idxname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateSeqStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.sequence.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateSchemaStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.schemaname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateFunctionStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        func_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.funcname
        ]

        self._check_identifier(
            func_name[-1],
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if node.conname is not None:
            self._check_identifier(
                node.conname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreatedbStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.dbname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateRoleStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.role,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.tablespacename,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTrigStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.trigname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateEnumStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        type_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.typeName
        ]

        self._check_identifier(
            type_name[-1],
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )
