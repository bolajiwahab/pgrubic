"""Linter."""

import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors

from pgshield.core import noqa, config


@dataclasses.dataclass(kw_only=True, frozen=True)
class Statement:
    """Representation of statement."""

    line_no: int
    column_offset: int
    text: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    statement_location: int
    statement_length: int
    column_offset: ast.Node
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
    """Holds all list rules, and runs them against a source file."""

    def __init__(self, config: config.Config) -> None:
        """Init."""
        self.checkers: set[Checker] = set()
        self.config = config

    @staticmethod
    def print_violations(*, checker: Checker, file_name: str) -> None:
        """Print all violations collected by a checker."""
        with pathlib.Path(file_name).open("r", encoding="utf-8") as source_file:

            source_code = source_file.read()

        for violation in checker.violations:

            # print(violation.statement_location)

            statement = get_statement_details(
                violation.statement_location,
                violation.statement_length,
                violation.column_offset,
                source_code,
            )

            sys.stdout.write(
                f"{file_name}:{statement.line_no}:"
                f"{statement.column_offset}:"
                f" {checker.code}: {violation.description}:"
                f" \n{statement.text} \n",
            )

    def run(self, source_path: str) -> bool:
        """Run rules on a source file."""
        file_name = pathlib.Path(source_path).name

        with pathlib.Path(source_path).open("r", encoding="utf-8") as source_file:

            source_code = source_file.read()

        # source_code = noqa.remove_sql_comments(source_code)

        try:

            tree: ast.Node = parser.parse_sql(source_code)

            _tree = parser.parse_sql_protobuf(source_code)
            # print(parser.deparse_protobuf(_tree))

        except parser.ParseError as error:

            sys.stdout.write(f"{file_name}: {error!s}")
            sys.exit(1)

        violations_found: bool = False

        # noqa_ignore_rules: list[tuple[int, str]] = noqa.extract(source_code)
        noqa_ignore_rules = []

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
                )

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
    print(getattr(node, "location"))
    return getattr(node, "location", 0)


def get_statement_details(
    statement_location: int,
    statement_length: int,
    column_offset: int,
    source_code: str,
) -> Statement:
    """Get statement details."""
    # source_code = noqa.replace_comments_with_spaces(source_code)
    print(statement_location, statement_length, column_offset)

    print((statement_location + statement_length) - column_offset)

    print(statement_length)

    # _column_offset = (column_offset - statement_location + 1)
    # if statement_location != 0 then statement_length + statement_length - column_offset -1
    _column_offset = 0 if statement_location == 0 else column_offset - statement_location

    statement_location = (
        statement_location + statement_length
    )
    # print(statement_location)
    # line_no = 1 + source_code.count("\n", 0, statement_location)
    line_no = source_code[:statement_location].count("\n") + 1
    print(line_no)
    # print(source_code[:].count("\n"))
    # print(line_num)

    # line_no = source_code[:statement_location].count("\n") + 1

    # print(line_no)

    # print(statement_location)

    line_start = source_code[:statement_location].rfind(";\n") + 1
    line_end = source_code.find(";\n", statement_location)

    print(source_code[line_start:line_end])
    print(line_start, statement_location, line_end)

    column = statement_location - line_start
    print(column)

    # text = source_code[:statement_length].strip("\n")
    # .replace('\r', '')
    # text = source_code[line_start:line_end].strip("\n").replace("\r", "")
    text = ""
    # column_offset = statement_location - line_start

    # print(text)

    # print(column_offset)

    # column_offset = column_offset + 1

    # print(column_offset)

    # arrow = "\n" + " " * column_offset + "^" # * (len(text) + 1)

    # text = text + arrow

    return Statement(line_no=line_no, column_offset=_column_offset, text=source_code[line_start:line_end].strip("\n"))
