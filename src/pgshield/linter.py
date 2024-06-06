"""Linter."""

import re
import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors  # type: ignore[import-untyped]

from pgshield import utils


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

    def __init__(self) -> None:
        """Init."""
        self.ignore_rules: list[tuple[int, str]] = []

        self.violations: list[Violation] = []

        self.config: dict[str, typing.Any] = {}

    required_attributes = ("name", "code")

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Check required attributes."""
        for required in cls.required_attributes:

            msg = f"Can't instantiate class {cls.__name__} without '{required}' attribute defined"  # noqa: E501

            if not hasattr(cls, required):

                raise TypeError(msg)

    def visit(self, ancestors: typing.Any, node: ast.Node) -> None:  # noqa: ANN401
        """Visit the node."""


class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self, config: dict[str, typing.Any]) -> None:
        """Init."""
        self.checkers: set[Checker] = set()
        self.config = config

    @staticmethod
    def print_violations(*, checker: Checker, file_name: str) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:

            sys.stdout.write(
                f"{file_name}:{violation.location}: {checker.code}: "
                f"{violation.description}: {stream.RawStream()(violation.statement)}\n",
            )

    def run(self, source_path: str) -> bool:
        """Run all rules on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r", encoding ="utf-8") as source_file:

            source_code = source_file.read()

        # Remove comments
        source_code = re.sub(
            r"^\s*--.*\n?|^\s*\/[*][\S\s]*?[*]\/", "", source_code, flags=re.MULTILINE,
        )

        try:

            tree: ast.Node  = parser.parse_sql(source_code)

        except parser.ParseError as error:

            sys.stdout.write(f"{file_name}: {error!s}")
            sys.exit(1)

        violations_found: bool = False

        ignore_rules_through_qa: list[tuple[int, str]] = utils.extract_noqa(source_code)

        for checker in self.checkers:

            checker.ignore_rules = ignore_rules_through_qa

            checker.config = self.config

            checker(tree)

            if checker.violations:

                violations_found = True

                self.print_violations(checker=checker, file_name=file_name)

        return violations_found

