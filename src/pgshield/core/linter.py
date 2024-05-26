"""Linter."""

import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors  # type: ignore[import-untyped]

from pgshield import logging


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    lineno: int
    node: ast.Node
    description: str


class Checker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate that lint rule."""

    def __init__(self, issue_code: str) -> None:
        """Init."""
        self.issue_code = issue_code
        self.violations: list[Violation] = []

    def visit(self, ancestors: typing.Any, node: ast.Node) -> None:  # noqa: ANN401
        """Visit the node."""


class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self) -> None:
        """Init."""
        self.checkers: set[Checker] = set()

    @staticmethod
    def print_violations(*, checker: Checker, file_name: str) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:
            logging.logger.error(
                f"{file_name}:{violation.lineno}: {checker.issue_code}: "
                f"{violation.description}: {stream.RawStream()(violation.node)}",
            )

    def run(self, source_path: str) -> bool:
        """Run all lints on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r") as source_file:
            source_code = source_file.read()

        tree = parser.parse_sql(source_code)
        for checker in self.checkers:
            checker(tree)
            self.print_violations(checker=checker, file_name=file_name)

        if checker.violations:
            return True

        return False
