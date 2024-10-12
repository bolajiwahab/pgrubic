"""Linter."""

import sys
import typing
import dataclasses

from pglast import ast, parser, stream, visitors, _extract_comments
from colorama import Fore, Style
from caseconverter import kebabcase

from pgrubic import DOCUMENTATION_URL
from pgrubic.core import noqa, config


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class Violation:
    """Representation of rule violation."""

    line_number: int
    column_offset: int
    source_text: str
    statement_location: int
    description: str
    help = ""


@dataclasses.dataclass(kw_only=True, slots=True)
class ViolationMetric:
    """Violation Metric."""

    total: int = 0
    fixed_total: int = 0
    fixable_auto_total: int = 0
    fixable_manual_total: int = 0
    fix: str | None = None


class BaseChecker(visitors.Visitor):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate it."""

    # Should not be set directly
    # as it is set in __init_subclass__
    code: str

    # Is this rule automatically fixable?
    is_auto_fixable: bool = False

    # Attributes shared among all subclasses
    config: config.Config
    inline_ignores: list[noqa.NoQaDirective]
    source_code: str

    def __init__(self) -> None:
        """Initialize variables."""
        self.violations: set[Violation] = set()
        self.statement_location: int = 0
        self.line_number: int = 0
        self.column_offset: int = 0
        self.source_text: str = ""

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Set code attribute for subclasses."""
        cls.code = cls.__module__.split(".")[-1]

    def visit(self, node: ast.Node, ancestors: visitors.Ancestor) -> None:
        """Visit the node."""

    @property
    def is_fix_applicable(self) -> bool:
        """Check if fix can be applied."""
        if not self.config.lint.fix:
            return False

        for inline_ignore in self.inline_ignores:
            if (
                self.statement_location == inline_ignore.location
                and inline_ignore.rule in (noqa.A_STAR, self.code)
                and not self.config.lint.ignore_noqa
            ):
                return False

        return True


class Linter:
    """Holds all lint rules, and runs them against a source file."""

    def __init__(self, config: config.Config) -> None:
        """Initialize variables."""
        self.checkers: set[BaseChecker] = set()
        self.config = config

    @staticmethod
    def skip_suppressed_violations(
        *,
        file: str,
        checker: BaseChecker,
        inline_ignores: list[noqa.NoQaDirective],
    ) -> None:
        """Skip suppressed violations."""
        for inline_ignore in inline_ignores:
            suppressed_violations: set[Violation] = {
                violation
                for violation in checker.violations
                if (
                    (
                        violation.statement_location == inline_ignore.location
                        or file == inline_ignore.file
                    )
                    and (inline_ignore.rule in (noqa.A_STAR, checker.code))
                )
            }

            if suppressed_violations:
                inline_ignore.used = True

                checker.violations = {
                    violation
                    for violation in checker.violations
                    if violation not in suppressed_violations
                }

    @staticmethod
    def print_violations(
        *,
        checker: BaseChecker,
        file: str,
    ) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:
            sys.stdout.write(
                f"\n{file}:{violation.line_number}:{violation.column_offset}:"
                f" \033]8;;{DOCUMENTATION_URL}/rules/{checker.__module__.split(".")[-2]}/{kebabcase(checker.__class__.__name__)}{Style.RESET_ALL}\033\\{Fore.RED}{Style.BRIGHT}{checker.code}{Style.RESET_ALL}\033]8;;\033\\:"  # noqa: E501
                f" {violation.description}\n\n",
            )
            for idx, line in enumerate(
                violation.source_text.splitlines(keepends=False),
                start=violation.line_number - violation.source_text.count("\n"),
            ):
                sys.stdout.write(
                    f"{Fore.BLUE}{idx} | {Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}\n",  # noqa: E501
                )
            sys.stdout.write("\n")

    def run(self, *, file: str, source_code: str) -> ViolationMetric:
        """Run rules on a source code."""
        try:
            tree: ast.Node = parser.parse_sql(source_code)
            comments = _extract_comments(source_code)

        except parser.ParseError as error:
            sys.stderr.write(f"{file}: {Fore.RED}{error!s}{Style.RESET_ALL}")

            sys.exit(1)

        inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
            file=file,
            source_code=source_code,
        )

        violations: ViolationMetric = ViolationMetric()

        BaseChecker.inline_ignores = inline_ignores
        BaseChecker.source_code = source_code

        for checker in self.checkers:
            checker.violations = set()

            checker(tree)

            if not self.config.lint.ignore_noqa:
                self.skip_suppressed_violations(
                    file=file,
                    checker=checker,
                    inline_ignores=inline_ignores,
                )

            self.print_violations(
                checker=checker,
                file=file,
            )

            if self.config.lint.fix is checker.is_auto_fixable is True:
                violations.fixed_total += len(checker.violations)

            if checker.is_auto_fixable is True:
                violations.fixable_auto_total += len(checker.violations)

            else:
                violations.fixable_manual_total += len(checker.violations)

            violations.total += len(checker.violations)

        # To be removed
        sys.stdout.write(
            stream.IndentedStream(
                comments=comments,
                semicolon_after_last_statement=True,
                comma_at_eoln=True,
                remove_pg_catalog_from_functions=True,
            )(tree),
        )
        # to be removed
        sys.stdout.write("\n")

        noqa.report_unused_ignores(
            file=file,
            inline_ignores=inline_ignores,
        )

        if parser.parse_sql(source_code) != tree:
            violations.fix = stream.IndentedStream(
                comments=comments,
                semicolon_after_last_statement=True,
            )(tree)

        return violations
