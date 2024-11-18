"""Linter."""

import sys
import typing
import dataclasses

from pglast import ast, parser, stream, visitors
from colorama import Fore, Style
from caseconverter import kebabcase

from pgrubic import DOCUMENTATION_URL
from pgrubic.core import noqa, config, loader, formatter


@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class Violation:
    """Representation of rule violation."""

    rule: str
    line_number: int
    column_offset: int
    line: str
    statement_location: int
    description: str
    help: str | None = None


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
    source_file: str
    source_code: str

    statement_location: int
    node_location: int
    line_number: int
    column_offset: int
    statement: str
    line: str

    def __init__(self) -> None:
        """Initialize variables."""
        self.violations: set[Violation] = set()

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

        if not self.is_auto_fixable:
            return False

        for inline_ignore in self.inline_ignores:
            if (
                (
                    self.statement_location == inline_ignore.location
                    or self.source_file == inline_ignore.source_file
                )
                and inline_ignore.rule in (noqa.A_STAR, self.code)
                and not self.config.lint.ignore_noqa
            ):
                return False

        return True


class Linter:
    """Holds all lint rules, and runs them against a source code."""

    def __init__(
        self,
        config: config.Config,
        # rules: typing.Any,
        formatters: typing.Callable[
            [],
            set[typing.Callable[[], None]],
        ] = loader.load_formatters,
    ) -> None:
        """Initialize variables."""
        self.checkers: set[BaseChecker] = set()
        self.config = config
        self.formatter = formatter.Formatter(
            config=config,
            formatters=formatters,
        )

    @staticmethod
    def _skip_suppressed_violations(
        *,
        source_file: str,
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
                        or source_file == inline_ignore.source_file
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
        source_file: str,
    ) -> None:
        """Print all violations collected by a checker."""
        for violation in checker.violations:
            if not checker.is_fix_applicable:
                sys.stdout.write(
                    f"{noqa.NEW_LINE}{source_file}:{violation.line_number}:{violation.column_offset}:"
                    f" \033]8;;{DOCUMENTATION_URL}/rules/{checker.__module__.split(".")[-2]}/{kebabcase(checker.__class__.__name__)}{Style.RESET_ALL}\033\\{Fore.RED}{Style.BRIGHT}{checker.code}{Style.RESET_ALL}\033]8;;\033\\:"  # noqa: E501
                    f" {violation.description}{noqa.NEW_LINE}",
                )

                for idx, line in enumerate(
                    violation.line.splitlines(keepends=False),
                    start=violation.line_number - violation.line.count(noqa.NEW_LINE),
                ):
                    sys.stdout.write(
                        f"{Fore.BLUE}{idx} | {Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}{noqa.NEW_LINE}",  # noqa: E501
                    )
                sys.stdout.write(noqa.NEW_LINE)

    def run(self, *, source_file: str, source_code: str) -> ViolationMetric:
        """Run rules on a source code."""
        fixed_statements: list[str] = []

        inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
            source_file=source_file,
            source_code=source_code,
        )

        violations: ViolationMetric = ViolationMetric()
        _violations: set[Violation] = set()

        BaseChecker.inline_ignores = inline_ignores
        BaseChecker.source_code = source_code
        BaseChecker.source_file = source_file

        for statement in noqa.extract_statement_locations(
            source_file=source_file,
            source_code=source_code,
        ):
            try:
                tree: ast.Node = parser.parse_sql(statement.text)
                comments = noqa.extract_comments(
                    source_file=source_file,
                    source_code=statement.text,
                )

            except parser.ParseError as error:
                sys.stderr.write(f"{source_file}: {Fore.RED}{error!s}{Style.RESET_ALL}")

                sys.exit(1)

            BaseChecker.statement = statement.text
            BaseChecker.statement_location = statement.start_location

            for checker in self.checkers:
                checker.violations = set()

                checker(tree)

                if not self.config.lint.ignore_noqa:
                    self._skip_suppressed_violations(
                        source_file=source_file,
                        checker=checker,
                        inline_ignores=inline_ignores,
                    )

                self.print_violations(
                    checker=checker,
                    source_file=source_file,
                )

                _violations.update(checker.violations)

                if self.config.lint.fix is checker.is_auto_fixable is True:
                    violations.fixed_total += len(checker.violations)

                if checker.is_auto_fixable is True:
                    violations.fixable_auto_total += len(checker.violations)

                else:
                    violations.fixable_manual_total += len(checker.violations)

                violations.total += len(checker.violations)

            if parser.parse_sql(statement.text) != tree:
                fixed_statement = stream.IndentedStream(
                    comments=comments,
                    semicolon_after_last_statement=False,
                    special_functions=True,
                    separate_statements=self.config.format.lines_between_statements,
                    remove_pg_catalog_from_functions=self.config.format.remove_pg_catalog_from_functions,
                    comma_at_eoln=not (self.config.format.comma_at_beginning),
                )(tree)

                if self.config.format.new_line_before_semicolon:
                    fixed_statement += noqa.NEW_LINE + noqa.SEMI_COLON
                else:
                    fixed_statement += noqa.SEMI_COLON

                fixed_statements.append(fixed_statement)

            else:
                fixed_statements.append(statement.text.strip())

        fixed_source_code = (
            noqa.NEW_LINE + (noqa.NEW_LINE * self.config.format.lines_between_statements)
        ).join(
            fixed_statements,
        ) + noqa.NEW_LINE

        if parser.parse_sql(fixed_source_code) != parser.parse_sql(source_code):
            violations.fix = fixed_source_code

            sys.stdout.write(violations.fix)

        noqa.report_unused_ignores(
            source_file=source_file,
            inline_ignores=inline_ignores,
        )

        # print(_violations)  # noqa: ERA001

        return violations
