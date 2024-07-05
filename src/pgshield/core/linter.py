"""Linter."""

import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors

from pgshield.core import noqa, config
from colorama import Fore, Style


@dataclasses.dataclass(kw_only=True, frozen=True)
class Line:
    """Representation of line of statement."""

    number: int
    column_offset: int
    text: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Statement:
    """Representation of statement."""

    location: int
    length: int


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    statement_location: int
    statement_length: int
    node_location: int
    description: str


class Checker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate that lint rule."""

    name: str
    code: str
    is_auto_fixable: bool

    def __init__(self) -> None:
        """Init."""
        self.noqa_ignore_rules: list[tuple[int, str]] = []

        self.violations: list[Violation] = []

        self.config: config.Config = dataclasses.field(
            default_factory=lambda: config.Config(**config.load_default_config()),
        )

        self.statement_location: int = 0

        self.statement_length: int = 0

        self.node_location: int = 0

    required_attributes: tuple[str, ...] = ("name", "code", "is_auto_fixable")

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Check required attributes."""
        for required in cls.required_attributes:

            msg = f"Can't instantiate class {cls.__name__} without '{required}' attribute defined"  # noqa: E501

            if not hasattr(cls, required):

                raise TypeError(msg)

    def visit(self, node: ast.Node, ancestors: typing.Any) -> None:  # noqa: ANN401
        """Visit the node."""


class Linter:
    """Holds all lint rules, and runs them against a source file."""

    def __init__(self, config: config.Config) -> None:
        """Init."""
        self.checkers: set[Checker] = set()
        self.config = config

    @staticmethod
    def print_violations(*, checker: Checker, file_name: str, source_code: str) -> None:
        """Print all violations collected by a checker."""
        # with pathlib.Path(file_name).open("r", encoding="utf-8") as source_file:

        #     source_code = source_file.read()

        for violation in checker.violations:

            line: Line = get_line_details(
                violation.statement_location,
                violation.statement_length,
                violation.node_location,
                source_code,
            )

            sys.stdout.write(
                f"{file_name}:{line.number}:{line.column_offset}:"
                f" {checker.code}: {violation.description}:"
                f" {Fore.GREEN}\n\n{line.text}\n\n{Style.RESET_ALL}",
            )

    def run(self, source_path: str) -> bool:
        """Run rules on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:

            source_code = source_file.read()

        source_code = noqa.remove_sql_comments(source_code)

        try:

            tree: ast.Node = parser.parse_sql(source_code)

        except parser.ParseError as error:

            sys.stdout.write(f"{file_name}: {Fore.RED}{error!s}{Style.RESET_ALL}")
            sys.exit(1)

        violations_found: bool = False

        noqa_ignore_rules: list[tuple[int, str]] = noqa.extract(source_code)

        print(noqa_ignore_rules)

        for checker in self.checkers:

            checker.noqa_ignore_rules = noqa_ignore_rules

            checker.config = self.config

            checker.violations = []

            checker(tree)

            if checker.violations:

                violations_found = True

                self.print_violations(
                    checker=checker,
                    file_name=file_name,
                    source_code=source_code,
                )

        return violations_found


def get_statement_details(ancestors: ast.Node) -> Statement:
    """Get statement details.

    pglast's AST is not a python list hence we cannot use list functions such as `len`
    directly on it. We need to build a list from the AST.
    """
    nodes: list[str] = []

    for node in ancestors:

        if node is None:
            break

        nodes.append(node)

    # The current node's parent is located two indexes from the end of the list.
    return Statement(
        location=ancestors[len(nodes) - 2].stmt_location,
        length=ancestors[len(nodes) - 2].stmt_len,
    )


def get_node_location(node: ast.Node) -> int:
    """Get node location."""
    return getattr(node, "location", 0)


def get_line_details(
    statement_location: int,
    statement_length: int,
    column_offset: int,
    source_code: str,
) -> Line:
    """Get line details."""
    actual_column_offset = (
        column_offset - statement_location if column_offset != 0 else statement_length
    )

    statement_location_end = statement_location + statement_length

    number = source_code[:statement_location_end].count("\n") + 1

    line_start = source_code[:statement_location_end].rfind(";\n") + 1

    line_end = source_code.find("\n", statement_location_end)

    text = source_code[line_start:line_end].strip("\n")

    return Line(number=number, column_offset=actual_column_offset, text=text)
