"""Visitors."""

import typing
from collections import deque

from pglast import ast, parser, visitors, parse_plpgsql

from pgrubic.core import formatter

RawStreamFactory = typing.Callable[[], formatter.RawStream]


class InlineSQLVisitor(visitors.Visitor):
    """Visitor for extracting inline SQL statements from PLpgSQL and function calls."""

    def __init__(self, raw_stream_factory: RawStreamFactory) -> None:
        """Instantiate variables."""
        self.raw_stream_factory = raw_stream_factory
        self._sql_statements: list[str] = []

    def _render_raw(self, source: str | ast.Node) -> str:
        """Render SQL with a fresh configured raw stream."""
        return typing.cast(str, self.raw_stream_factory()(source))

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if node.sql_body:
            return

        _sql_statements = self._extract_sql_statements_from_plpgsql(
            parse_plpgsql(self._render_raw(node)),
        )
        self._sql_statements.extend(_sql_statements)

    def visit_DoStmt(self, ancestors: visitors.Ancestor, node: ast.DoStmt) -> None:
        """Visit DoStmt."""
        _sql_statements = self._extract_sql_statements_from_plpgsql(
            parse_plpgsql(self._render_raw(node)),
        )
        self._sql_statements.extend(_sql_statements)

    def visit_FuncCall(
        self,
        ancestors: visitors.Ancestor,
        node: ast.FuncCall,
    ) -> None:
        """Visit FuncCall."""
        if node.args:
            for arg in node.args:
                if (
                    isinstance(arg, ast.A_Const)
                    and isinstance(arg.val, ast.String)
                    and isinstance(arg.val.sval, str)
                ):
                    try:
                        # might not be an SQL statement.
                        statement = self._render_raw(arg.val.sval)
                        # if statement is PLpgSQL, it would be processed at a later pass
                        self._sql_statements.append(statement)
                    except parser.ParseError:
                        continue

    def _extract_sql_statements_from_plpgsql(
        self,
        node: object,
    ) -> list[str]:
        """Extract SQL statements from PLpgSQL tokens using iterative breadth-first walk.

        Parameters:
        ----------
        node: object
            PLpgSQL tokens.

        Returns:
        -------
        list[str]
            List of SQL statements.
        """
        queue = deque([node])
        statements: list[str] = []

        while queue:
            current = queue.popleft()

            if isinstance(current, dict):
                for key, value in current.items():
                    # https://github.com/pganalyze/libpg_query/blob/17-latest/src/postgres/include/plpgsql.h#L891-L902
                    if key == "sqlstmt":
                        expr = value["PLpgSQL_expr"]
                        statements.append(expr["query"])
                    else:
                        queue.append(value)
            elif isinstance(current, list):
                queue.extend(current)

        return statements

    def get_sql_statements(self) -> list[str]:
        """Get SQL statements."""
        return self._sql_statements


def visit_inline_sql(
    *,
    node: tuple[ast.RawStmt, ...],
    raw_stream_factory: RawStreamFactory,
) -> list[str]:
    """Visit inline SQL."""
    inline_sql_visitor = InlineSQLVisitor(raw_stream_factory=raw_stream_factory)
    inline_sql_visitor(node)

    return inline_sql_visitor.get_sql_statements()


def extract_nested_inline_sql_statements(
    *,
    node: tuple[ast.RawStmt, ...],
    raw_stream_factory: RawStreamFactory,
) -> list[str]:
    """Extract nested inline SQL statements from PLpgSQL and function calls
    using iterative breadth-first walk.
    """
    statements: list[str] = []

    queue = deque([node])

    while queue:
        current_tree = queue.popleft()

        for statement in visit_inline_sql(
            node=current_tree,
            raw_stream_factory=raw_stream_factory,
        ):
            statements.append(statement)
            child_tree = parser.parse_sql(statement)
            queue.append(child_tree)

    return statements
