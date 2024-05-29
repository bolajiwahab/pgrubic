"""Linter."""

import re
import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors  # type: ignore[import-untyped]

from pgshield import utils, logging


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    location: int
    statement: ast.Node
    description: str


class Checker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate that lint rule."""

    name: str
    code: str

    description: str

    def __init__(self) -> None:
        """Init."""
        self.ignore_rules: list[utils.Comment] = []
        self.violations: list[Violation] = []

        for required in ("name", "code"):
            if not hasattr(self, required):
                msg = f"{self.__class__.__name__} must define a '{required}' attribute."
                raise NotImplementedError(msg)

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
                f"{file_name}:{violation.location}: {checker.code}: "
                f"{violation.description}: {stream.RawStream()(violation.statement)}",
            )

    def run(self, source_path: str) -> None:
        """Run all rules on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r") as source_file:
            source_code = source_file.read()

        source_code = re.sub(
            r"^\s*--.*\n?|^\s*\/[*][\S\s]*?[*]\/", " ", source_code, flags=re.MULTILINE,
        )

        tree = parser.parse_sql(source_code)

        violations: bool = False

        for checker in self.checkers:

            checker.ignore_rules = utils.extract_noqa(source_code)

            checker(tree)

            if checker.violations:

                violations = True

                self.print_violations(checker=checker, file_name=file_name)

        if violations:
            sys.exit(1)
