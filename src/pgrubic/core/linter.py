"""Linter."""

from __future__ import annotations

import sys
import typing
import fnmatch
import pathlib
import functools
from contextlib import contextmanager

from pglast import ast, parser, stream, visitors
from colorama import Fore, Style
from caseconverter import kebabcase

from pgrubic import ISSUES_URL, PACKAGE_NAME, DOCUMENTATION_URL
from pgrubic.core import noqa, config, errors, visitors as pgrubic_visitors, formatter

if typing.TYPE_CHECKING:
    from collections import abc  # pragma: no cover


DEFAULT_LINT_REPORT_FILE: str = f"{PACKAGE_NAME}-lint-report.md"


class FixCounter:
    """Fix counter."""

    def __init__(self) -> None:
        """Initialize variables."""
        self.counter = 0

    def add(self) -> None:
        """Increment fix counter."""
        self.counter += 1

    def reset(self) -> None:
        """Reset fix counter."""
        self.counter = 0


class Violation(typing.NamedTuple):
    """Representation of rule violation."""

    rule_code: str
    rule_name: str
    rule_category: str
    line_number: int
    column_offset: int
    line: str
    statement_location: int
    description: str
    is_auto_fixable: bool
    is_fix_enabled: bool
    help: str | None = None


class LintResult(typing.NamedTuple):
    """Lint Result."""

    source_file: str
    violations: set[Violation]
    errors: set[errors.Error]
    fixed_source_code: str | None = None


class ViolationStats(typing.NamedTuple):
    """Violation Stats."""

    total: int
    auto_fixable: int
    fix_enabled: int


class CheckerMeta(type):
    """Metaclass for Checker. This metaclass handles both runtime and subclass method
    decorations ensuring decorated methods retain their decoration even in child
    processes. It is originally created for method decorations but could be extended in
    the future.
    """

    def __new__(
        cls: type[CheckerMeta],
        name: str,
        bases: tuple[typing.Any],
        dct: dict[str, typing.Any],
    ) -> typing.Any:
        """Add method decorations."""
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and attr_name.startswith("_fix"):
                dct[attr_name] = cls._apply_fix(attr_value)

            if callable(attr_value) and attr_name.startswith("visit_"):
                dct[attr_name] = cls._set_locations(attr_value)

        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def _set_locations(
        func: abc.Callable[..., typing.Any],
    ) -> abc.Callable[..., typing.Any]:
        """Helper method to set locations for node."""

        @functools.wraps(func)
        def wrapper(
            checker: BaseChecker,
            ancestors: visitors.Ancestor,
            node: ast.Node,
        ) -> typing.Any:
            """Set locations for node."""
            # some nodes have location attribute which is different from node location
            # for example ast.CreateTablespaceStmt while some nodes do not carry
            # location at all.
            # If a node has no location or it is an inlined sql statement,
            # we use the length of the root statement
            if (
                hasattr(node, "location")
                and isinstance(node.location, int)
                and not checker.in_inline_sql_mode
            ):
                checker.node_location = checker.statement_location + node.location
            else:
                checker.node_location = checker.statement_location + len(
                    checker.root_statement,
                )

            # get the position of the newline just before our node location,
            line_start = (
                checker.source_code.rfind(noqa.NEW_LINE, 0, checker.node_location) + 1
            )
            # get the position of the newline just after our node location
            line_end = checker.source_code.find(noqa.NEW_LINE, checker.node_location)

            # line number is number of newlines before our node location,
            # increment by 1 to land on the actual node
            checker.line_number = (
                checker.source_code[: checker.node_location].count(noqa.NEW_LINE) + 1
            )
            # We account for a single space thus +1
            checker.column_offset = (checker.node_location - line_start) + 1

            # If a node has no location or it is an inlined sql statement,
            # we return the whole root statement instead
            if (
                hasattr(node, "location")
                and isinstance(node.location, int)
                and not checker.in_inline_sql_mode
            ):
                checker.line = checker.source_code[line_start:line_end]
            else:
                checker.line = checker.root_statement

            return func(checker, ancestors, node)

        return wrapper

    @staticmethod
    def _apply_fix(
        func: abc.Callable[..., typing.Any],
    ) -> abc.Callable[..., typing.Any]:
        """Helper method to apply fix only if it is applicable."""

        @functools.wraps(func)
        def wrapper(
            checker: BaseChecker,
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> typing.Any:
            """Apply fix only if it is applicable."""
            if not checker.config.lint.fix:
                return None

            if not checker.is_fix_applicable:
                return None

            result = func(checker, *args, **kwargs)

            checker.statement_fixes.add()
            checker.file_fixes.add()

            return result

        return wrapper


class BaseChecker(visitors.Visitor, metaclass=CheckerMeta):  # type: ignore[misc]
    """Define a lint rule, and store all the nodes that violate it."""

    # Should not be set directly
    # as they are set in __init_subclass__
    code: str
    name: str
    category: str

    # Is this rule automatically fixable?
    is_auto_fixable: bool = False

    # Attributes shared among all subclasses
    config: config.Config
    lint_ignores: list[noqa.NoQaDirective]
    source_file: str
    source_code: str

    statement_location: int
    node_location: int
    line_number: int
    column_offset: int
    statement: str
    root_statement: str
    line: str
    in_inline_sql_mode: bool = False

    # Track fixes
    statement_fixes: FixCounter
    file_fixes: FixCounter

    def __init__(self) -> None:
        """Initialize variables."""
        self.violations: set[Violation] = set()

    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        """Set code, name and category attributes for subclasses."""
        cls.code = cls.__module__.split(".")[-1]
        cls.name = kebabcase(cls.__name__)
        cls.category = cls.__module__.split(".")[-2]

    def visit(self, ancestors: visitors.Ancestor, node: ast.Node) -> None:
        """Visit the node."""

    @property
    def is_fix_enabled(self) -> bool:
        """Check if fix is enabled according to config."""
        # if a rule is not auto fixable, there is no need to check
        # if its fix is enabled, in which case, we return False
        if not self.is_auto_fixable:
            return False

        return not (
            (
                self.config.lint.fixable
                and not any(
                    fnmatch.fnmatch(self.code, pattern + "*")
                    for pattern in self.config.lint.fixable
                )
            )
            or any(
                fnmatch.fnmatch(self.code, pattern + "*")
                for pattern in self.config.lint.unfixable
            )
        )

    @property
    def is_fix_applicable(self) -> bool:
        """Check if fix can be applied."""
        if not self.is_auto_fixable:
            return False

        if not self.is_fix_enabled:
            return False

        # if the violation has been suppressed by noqa, there is no need to try to fix it
        for inline_ignore in self.lint_ignores:
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

    @classmethod
    @contextmanager
    def disable_auto_fix(
        cls,
        checkers: set[BaseChecker],
    ) -> typing.Generator[None, None, None]:
        """Disable auto fix for the given checkers."""
        original_states = [checker.is_auto_fixable for checker in checkers]

        try:
            for checker in checkers:
                checker.is_auto_fixable = False
            yield
        finally:
            for checker, original_state in zip(checkers, original_states, strict=True):
                checker.is_auto_fixable = original_state


class Linter:
    """Holds all lint rules, and runs them against a source code."""

    def __init__(
        self,
        config: config.Config,
        formatters: typing.Callable[
            [],
            set[typing.Callable[[], None]],
        ],
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
        lint_ignores: list[noqa.NoQaDirective],
    ) -> None:
        """Skip suppressed violations.

        Parameters:
        ----------
        source_file: str
            Path to the source file.

        checker: BaseChecker
            Lint rule checker.

        lint_ignores: list[NoQaDirective]
            List of noqa directives.

        Returns:
        -------
        None
        """
        for inline_ignore in lint_ignores:
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
    def get_violation_stats(violations: set[Violation]) -> ViolationStats:
        """Get violation stats.

        Parameters:
        ----------
        violations: set[Violation]
            Violations to get stats from.

        Returns:
        -------
        ViolationStats
            Violation stats.
        """
        return ViolationStats(
            total=len(violations),
            auto_fixable=sum(1 for violation in violations if violation.is_auto_fixable),
            fix_enabled=sum(1 for violation in violations if violation.is_fix_enabled),
        )

    @staticmethod
    def print_violations(
        *,
        violations: set[Violation],
        source_file: str,
    ) -> None:
        """Print all violations collected by a checker.

        Parameters:
        ----------
        violations: set[Violation]
            Violations to print.
        source_file: str
            Path to the source file.

        Returns:
        -------
        None
        """
        for violation in violations:
            sys.stdout.write(
                f"{noqa.NEW_LINE}{source_file}:{violation.line_number}:{violation.column_offset}:"
                f"{noqa.SPACE}\033]8;;{DOCUMENTATION_URL}/rules/{violation.rule_category}/{violation.rule_name}{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{violation.rule_code}\033]8;;{Style.RESET_ALL}:"
                f"{noqa.SPACE}{violation.description}{noqa.NEW_LINE}",
            )

            for idx, line in enumerate(
                violation.line.splitlines(keepends=False),
                start=violation.line_number - violation.line.count(noqa.NEW_LINE),
            ):
                sys.stdout.write(
                    f"{Fore.BLUE}{idx} | {Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}{noqa.NEW_LINE}",  # noqa: E501
                )
                # in order to have arrow pointing to the violation, we need to shift
                # the screen by the length of the line_number as well as 2 spaces
                # used above between the separator (|)
                (
                    sys.stdout.write(
                        noqa.SPACE
                        * (violation.column_offset + len(str(violation.line_number)) + 2)
                        + "^"
                        + noqa.NEW_LINE,
                    )
                    if idx == violation.line_number
                    else None
                )

    @staticmethod
    def generate_lint_report(
        *,
        lint_results: list[LintResult],
        report_file: str = DEFAULT_LINT_REPORT_FILE,
    ) -> None:
        """Generate a report in markdown for lint results. It overwrites the report file.

        Parameters:
        ----------
        lint_results: list[LintResult]
            List of lint results.
        report_file: str
            Path to the report file.

        Returns:
        -------
        None
        """
        total_violations = sum(
            len(lint_result.violations) for lint_result in lint_results
        )
        total_errors = sum(len(lint_result.errors) for lint_result in lint_results)

        lines: list[str] = [f"## {PACKAGE_NAME.capitalize()} Lint Report\n"]

        lines.append(f"Total violations: **{total_violations}**\n")
        lines.append(f"Total errors: **{total_errors}**\n")

        if total_violations > 0:
            lines.append(
                f"<details>\n<summary>Violations ({total_violations})</summary>\n",
            )
            lines.append("| File | Line | Col | Rule | Description | Help |")
            lines.append("|------|------|-----|------|-------------|------|")

            violation_rows = [
                f"|{noqa.SPACE}{pathlib.Path(lint_result.source_file).name}{noqa.SPACE}"
                f"|{noqa.SPACE}{violation.line_number}{noqa.SPACE}"
                f"|{noqa.SPACE}{violation.column_offset}{noqa.SPACE}"
                f"|{noqa.SPACE}[{violation.rule_code}]({DOCUMENTATION_URL}/rules/{violation.rule_category}/{violation.rule_name}){noqa.SPACE}"
                f"|{noqa.SPACE}{violation.description}{noqa.SPACE}"
                f"|{noqa.SPACE}{violation.help or '-'}{noqa.SPACE}|"
                for lint_result in lint_results
                for violation in lint_result.violations
            ]

            lines.extend(violation_rows)

            lines.append("</details>\n")

        if total_errors > 0:
            lines.append(f"<details>\n<summary>Errors ({total_errors})</summary>\n")
            lines.append("| File | Message | Hint |")
            lines.append("|------|---------|------|")

            error_rows = [
                f"|{noqa.SPACE}{pathlib.Path(lint_result.source_file).name}{noqa.SPACE}"
                f"|{noqa.SPACE}{error.message}{noqa.SPACE}"
                f"|{noqa.SPACE}{error.hint or '-'}{noqa.SPACE}|"
                for lint_result in lint_results
                for error in lint_result.errors
            ]

            lines.extend(error_rows)

            lines.append("</details>\n")

        pathlib.Path(report_file).write_text("\n".join(lines), encoding="utf-8")

    def run(self, *, source_file: str, source_code: str) -> LintResult:  # noqa: C901, PLR0912, PLR0915
        """Run rules on a source code.

        Parameters:
        ----------
        source_file: str
            Path to the source file.
        source_code: str
            Source code to lint.

        Returns:
        -------
        LintResult
            Lint result.
        """
        fixed_statements: list[str] = []

        violations: set[Violation] = set()
        _errors: set[errors.Error] = set()

        BaseChecker.source_code = source_code
        BaseChecker.source_file = source_file
        BaseChecker.config = self.config

        BaseChecker.file_fixes = FixCounter()
        BaseChecker.statement_fixes = FixCounter()

        statements = noqa.extract_statements(
            source_code=source_code,
        )

        file_lint_ignores = noqa.extract_file_lint_ignores(
            source_file=source_file,
            source_code=source_code,
        )

        lint_ignores = file_lint_ignores

        for statement in statements:
            statement_lint_ignores: list[noqa.NoQaDirective] = (
                noqa.extract_statement_lint_ignores(
                    statement=statement,
                    source_code=source_code,
                )
            )

            lint_ignores.extend(statement_lint_ignores)

            BaseChecker.lint_ignores = lint_ignores

            # Reset the applied fixes for each statement
            BaseChecker.applied_fixes = []

            BaseChecker.root_statement = statement.text
            BaseChecker.statement_location = statement.start_location

            try:
                parse_tree: ast.Node = parser.parse_sql(statement.text)

                comments = noqa.extract_comments(
                    statement=statement,
                )

                inline_sql_statements = (
                    pgrubic_visitors.extract_nested_inline_sql_statements(
                        parse_tree,
                    )
                )

            except parser.ParseError as error:
                _errors.add(
                    errors.Error(
                        source_file=str(source_file),
                        source_code=source_code,
                        statement_start_location=statement.start_location + 1,
                        statement_end_location=statement.end_location,
                        statement=statement.text,
                        message=str(error),
                        hint=f"""Make sure the statement is valid PostgreSQL statement. If it is, please report this issue at {ISSUES_URL}{noqa.NEW_LINE}""",  # noqa: E501
                    ),
                )
                fixed_statements.append(statement.text.strip(noqa.NEW_LINE))
                continue

            BaseChecker.root_statement = statement.text
            BaseChecker.statement_location = statement.start_location
            # Reset statement fixes counter per statement
            BaseChecker.statement_fixes.reset()

            # Signal that we are processing inline sql statements
            BaseChecker.in_inline_sql_mode = True

            # Temporarily disable auto fixes, we do not try to fix inline sql statements
            # inside plpgsql
            with BaseChecker.disable_auto_fix(self.checkers):
                for inline_sql_statement in inline_sql_statements:
                    BaseChecker.statement = inline_sql_statement
                    for checker in self.checkers:
                        checker.violations = set()
                        checker(parser.parse_sql(inline_sql_statement))

                        if not self.config.lint.ignore_noqa:
                            self._skip_suppressed_violations(
                                source_file=source_file,
                                checker=checker,
                                lint_ignores=lint_ignores,
                            )

                        violations.update(checker.violations)

            # We are done processing inline sql statements
            # Reset in_inline_sql_mode to false
            BaseChecker.in_inline_sql_mode = False

            BaseChecker.statement_location = statement.start_location
            BaseChecker.statement = statement.text
            for checker in self.checkers:
                checker.violations = set()

                checker(parse_tree)

                if not self.config.lint.ignore_noqa:
                    self._skip_suppressed_violations(
                        source_file=source_file,
                        checker=checker,
                        lint_ignores=lint_ignores,
                    )

                violations.update(checker.violations)

            # If the statement parse tree has been modified due to fixes,
            # we convert it to string
            if BaseChecker.statement_fixes.counter > 0:
                try:
                    fixed_statement = stream.IndentedStream(
                        comments=comments,
                        semicolon_after_last_statement=False,
                        special_functions=True,
                        separate_statements=self.config.format.lines_between_statements,
                        remove_pg_catalog_from_functions=self.config.format.remove_pg_catalog_from_functions,
                        comma_at_eoln=not (self.config.format.comma_at_beginning),
                    )(parse_tree)

                    if self.config.format.new_line_before_semicolon:
                        fixed_statement += noqa.NEW_LINE + noqa.SEMI_COLON
                    else:
                        fixed_statement += noqa.SEMI_COLON

                    fixed_statements.append(fixed_statement)
                except RecursionError as error:  # pragma: no cover
                    _errors.add(
                        errors.Error(
                            source_file=str(source_file),
                            source_code=source_code,
                            statement_start_location=statement.start_location + 1,
                            statement_end_location=statement.end_location,
                            statement=statement.text,
                            message=str(error),
                            hint="Maximum format depth exceeded, reduce deeply nested queries",  # noqa: E501
                        ),
                    )
                    fixed_statements.append(statement.text.strip(noqa.NEW_LINE))

            else:
                fixed_statements.append(statement.text.strip(noqa.NEW_LINE))

        fixed_source_code = None

        if BaseChecker.file_fixes.counter > 0:
            fixed_source_code = (
                noqa.NEW_LINE
                + (noqa.NEW_LINE * self.config.format.lines_between_statements)
            ).join(
                fixed_statements,
            ) + noqa.NEW_LINE  # final new line

        noqa.report_unused_lint_ignores(
            source_file=source_file,
            lint_ignores=lint_ignores,
        )

        return LintResult(
            source_file=source_file,
            violations=violations,
            errors=_errors,
            fixed_source_code=fixed_source_code,
        )
