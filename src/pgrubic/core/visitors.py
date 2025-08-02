"""Visitors."""

import typing

from pglast import ast, stream, visitors, parse_plpgsql


class PLPGSQLVisitor(visitors.Visitor):  # type: ignore[misc]
    """Visitor for extracting inline SQL statements from PLpgSQL."""

    def __init__(self) -> None:
        """Instantiate variables."""
        self._sql_statements: list[str] = []

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if node.sql_body:
            return

        _sql_statements = self._extract_sql_statements_from_plpgsql(
            parse_plpgsql(stream.RawStream()(node)),
        )
        self._sql_statements.extend(_sql_statements)

    def visit_DoStmt(self, ancestors: visitors.Ancestor, node: ast.DoStmt) -> None:
        """Visit DoStmt."""
        _sql_statements = self._extract_sql_statements_from_plpgsql(
            parse_plpgsql(stream.RawStream()(node)),
        )
        self._sql_statements.extend(_sql_statements)

    def _extract_sql_statements_from_plpgsql(
        self,
        node: dict[str, typing.Any],
    ) -> list[str]:
        """Extract SQL statements from PLpgSQL tokens using iterative deep walk.

        Parameters:
        ----------
        node: dict[str, typing.Any]
            PLpgSQL tokens.

        Returns:
        -------
        list[str]
            List of SQL statements.
        """
        stack = [node]
        statements: list[str] = []

        while stack:
            current = stack.pop()

            if isinstance(current, dict):
                for key, value in current.items():
                    if key == "sqlstmt":
                        expr = value.get("PLpgSQL_expr")
                        if expr and "query" in expr:
                            statements.append(expr["query"])
                    else:
                        stack.append(value)
            elif isinstance(current, list):
                stack.extend(current)

        return statements

    def get_sql_statements(self) -> list[str]:
        """Get SQL statements."""
        return self._sql_statements
