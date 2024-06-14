"""Linter."""

import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors  # type: ignore[import-untyped]

from pgshield.core import noqa, config


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    lineno: int
    column_offset: int
    statement: ast.Node
    description: str


class Checker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate that lint rule."""

    name: str
    code: str

    def __init__(self) -> None:
        """Init."""
        self.noqa_ignore_rules: list[tuple[int, str]] = []

        self.violations: list[Violation] = []

        self.config: config.Config = dataclasses.field(
            default_factory=lambda: config.Config(**config.load_default_config()),
        )

    required_attributes: tuple[str, ...] = ("name", "code")

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Check required attributes."""
        for required in cls.required_attributes:

            msg = f"Can't instantiate class {cls.__name__} without '{required}' attribute defined"  # noqa: E501

            if not hasattr(cls, required):

                raise TypeError(msg)

    def visit(self, node: ast.Node, ancestors: typing.Any) -> None:  # noqa: ANN401
        """Visit the node."""


class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self, config: config.Config) -> None:
        """Init."""
        self.checkers: set[Checker] = set()
        self.config = config

    @staticmethod
    def print_violations(*, checker: Checker, file_name: str) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:

            sys.stdout.write(
                f"{file_name}:{violation.lineno}:{violation.column_offset}: "
                f"{checker.code}: {violation.description}: {stream.RawStream()(violation.statement)}\n\n",  # noqa: E501
            )

    def run(self, source_path: str) -> bool:
        """Run all rules on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:

            source_code = source_file.read()

        source_code = noqa.remove_sql_comments(source_code)

        try:

            tree: ast.Node = parser.parse_sql(source_code)

        except parser.ParseError as error:

            sys.stdout.write(f"{file_name}: {error!s}")
            sys.exit(1)

        violations_found: bool = False

        noqa_ignore_rules: list[tuple[int, str]] = noqa.extract(source_code)

        for checker in self.checkers:

            checker.noqa_ignore_rules = noqa_ignore_rules

            checker.config = self.config

            checker(tree)

            if checker.violations:

                violations_found = True

                self.print_violations(checker=checker, file_name=file_name)

        return violations_found


def get_statement_index(ancestors: ast.Node) -> int:
    """Get statement index.

    pglast's AST is not a python list hence we cannot use list functions such as `len`
    directly on it. We need to build a list from the AST.
    """
    nodes: list[str] = []

    for node in ancestors:

        if node is None:
            break

        nodes.append(node)

    # The current node's parent is located two indexes from the end of the list.
    return len(nodes) - 2


def get_column_offset(ancestors: ast.Node, node: ast.Node) -> int:
    """Get column offset."""
    if hasattr(node, "location"):
        return typing.cast(int, node.location)

    return typing.cast(
        int,
        ancestors[get_statement_index(ancestors)].stmt_location
        + ancestors[get_statement_index(ancestors)].stmt_len,
    )
