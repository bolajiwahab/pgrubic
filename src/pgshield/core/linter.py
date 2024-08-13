"""Linter."""

import sys
import typing
import pathlib
import dataclasses

from pglast import ast, parser, stream, visitors, _extract_comments
from colorama import Fore, Style
from caseconverter import kebabcase

from pgshield.core import noqa, config


@dataclasses.dataclass(kw_only=True, frozen=True)
class Line:
    """Representation of line of statement."""

    number: int
    column_offset: int
    text: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Violation:
    """Representation of rule violation."""

    statement_location: int
    statement_length: int
    node_location: int
    description: str


@dataclasses.dataclass(kw_only=True)
class ViolationMetric:
    """Metric of violations."""

    violations_total: int = 0
    violations_fixed_total: int = 0
    violations_fixable_auto_total: int = 0
    violations_fixable_manual_total: int = 0
    violations_fixes: str | None = None


class Checker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate it."""

    code: str
    is_auto_fixable: bool
    config: config.Config
    inline_ignores: list[noqa.NoQaDirective]

    def __init__(self) -> None:
        """Initialize variables."""
        self.violations: set[Violation] = set()
        self.statement_location: int = 0
        self.statement_length: int = 0
        self.node_location: int = 0

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Check required attributes."""
        required_attributes: tuple[str, ...] = ("is_auto_fixable",)

        for required in required_attributes:

            msg = f"Can't instantiate class {cls.__name__} without '{required}' attribute defined"  # noqa: E501

            if not hasattr(cls, required):

                raise TypeError(msg)

    def visit(self, node: ast.Node, ancestors: visitors.Ancestor) -> None:
        """Visit the node."""

    @property
    def is_fix_applicable(self) -> bool:
        """Check if fix can be applied."""
        for inline_ignore in self.inline_ignores:

            if (
                (
                    self.config.fix
                    and self.statement_location == inline_ignore.location
                    and (inline_ignore.rule in (noqa.A_STAR, self.code))
                    and not self.config.ignore_noqa
                ) or not self.config.fix
            ):

                return False

        return True


class Linter:
    """Holds all lint rules, and runs them against a source file."""

    def __init__(self, config: config.Config) -> None:
        """Initialize variables."""
        self.checkers: set[Checker] = set()
        self.config = config

    @staticmethod
    def skip_suppressed_violations(
        *,
        checker: Checker,
        inline_ignores: list[noqa.NoQaDirective],
    ) -> None:
        """Skip suppressed violations."""
        for inline_ignore in inline_ignores:

            suppressed_violations: set[Violation] = {
                violation
                for violation in checker.violations
                if (
                    violation.statement_location == inline_ignore.location
                    and (inline_ignore.rule in (noqa.A_STAR, checker.code))
                )
            }

            if suppressed_violations:

                inline_ignore.used = True

                checker.violations = {
                    violation
                    for violation in checker.violations if violation not in
                    suppressed_violations
                }


    @staticmethod
    def print_violations(
        *,
        checker: Checker,
        source_path: pathlib.Path,
        source_code: str,
    ) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:

            line: Line = _get_line_details(
                violation.statement_location,
                violation.statement_length,
                violation.node_location,
                source_code,
            )

            sys.stdout.write(
                f"\n{source_path}:{line.number}:{line.column_offset}:"
                f" \033]8;;http://127.0.0.1:8000/rules/{checker.__module__.split(".")[-2]}/{kebabcase(checker.__class__.__name__)}{Style.RESET_ALL}\033\\{Fore.RED}{Style.BRIGHT}{checker.code}{Style.RESET_ALL}\033]8;;\033\\:"
                f" {violation.description}:"
                f" {Fore.GREEN}\n\n{line.text}\n\n{Style.RESET_ALL}",
            )


    def run(self, *, source_path: pathlib.Path, source_code: str) -> ViolationMetric:
        """Run rules on a source code."""
        try:

            tree: ast.Node = parser.parse_sql(source_code)
            comments = _extract_comments(source_code)

        except parser.ParseError as error:

            sys.stdout.write(f"{source_path}: {Fore.RED}{error!s}{Style.RESET_ALL}")

            sys.exit(1)

        inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores_from_inline_comments(source_code)  # noqa: E501

        violations: ViolationMetric = ViolationMetric()

        Checker.inline_ignores = inline_ignores

        for checker in self.checkers:

            checker.violations = set()

            checker(tree)

            if not self.config.ignore_noqa:

                self.skip_suppressed_violations(
                    checker=checker,
                    inline_ignores=inline_ignores,
                )

            self.print_violations(
                checker=checker,
                source_path=source_path,
                source_code=source_code,
            )

            if self.config.fix is checker.is_auto_fixable is True:

                violations.violations_fixed_total += len(checker.violations)

            if checker.is_auto_fixable is True:

                violations.violations_fixable_auto_total += len(checker.violations)

            else:

                violations.violations_fixable_manual_total += len(checker.violations)

            violations.violations_total += len(checker.violations)

        print(stream.IndentedStream(comments=comments, semicolon_after_last_statement=True)(tree))

        noqa.report_unused_ignores(source_path=source_path, inline_ignores=inline_ignores)

        if parser.parse_sql(source_code) != tree:

            violations.violations_fixes = stream.IndentedStream(
                comments=comments,
                semicolon_after_last_statement=True,
            )(tree)

        return violations


def _get_line_details(
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
