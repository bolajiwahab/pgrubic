"""Test linter."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM014 import SingleLetterIdentifier
from pgrubic.rules.naming.NM016 import DateColumnWithoutSuffix


@pytest.fixture(scope="module")
def date_column_without_suffix() -> core.BaseChecker:
    """Create an instance of date column without suffix."""
    core.add_apply_fix_to_rule(DateColumnWithoutSuffix)
    core.add_set_locations_to_rule(DateColumnWithoutSuffix)
    return DateColumnWithoutSuffix()


@pytest.fixture
def lint_date_column_without_suffix(
    linter: core.Linter,
    date_column_without_suffix: core.BaseChecker,
) -> core.Linter:
    """Lint date column without suffix."""
    date_column_without_suffix.config.lint.fix = False
    date_column_without_suffix.config.lint.date_column_suffix = "_date"
    linter.checkers.add(date_column_without_suffix)

    return linter


def test_date_column_without_suffix_rule_code(
    date_column_without_suffix: core.BaseChecker,
) -> None:
    """Test date column without suffix rule code."""
    assert (
        date_column_without_suffix.code
        == date_column_without_suffix.__module__.split(".")[-1]
    )


def test_date_column_without_suffix_auto_fixable(
    date_column_without_suffix: core.BaseChecker,
) -> None:
    """Test date column without suffix auto fixable."""
    assert date_column_without_suffix.is_auto_fixable is True


def test_pass_non_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
) -> None:
    """Test pass non date column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated boolean);"

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
) -> None:
    """Test fail date column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated date);"

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_date_column_without_suffix_description(
    lint_date_column_without_suffix: core.Linter,
    date_column_without_suffix: core.BaseChecker,
) -> None:
    """Test date column without suffix description."""
    sql_fail: str = "CREATE TABLE tbl (activated date);"

    _: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(date_column_without_suffix.violations),
        ).description
        == f"Date column name should be suffixed with `{date_column_without_suffix.config.lint.date_column_suffix}`"  # noqa: E501
    )


def test_pass_noqa_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
) -> None:
    """Test pass noqa date column without suffix."""
    sql_pass_noqa: str = """
    -- noqa: NM016
    CREATE TABLE tbl (activated date);
    """

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
) -> None:
    """Test fail noqa date column without suffix."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN activated date;
    """

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
) -> None:
    """Test pass noqa date column without suffix."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (activated date);
    """

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
    date_column_without_suffix: core.BaseChecker,
) -> None:
    """Test fail fix date column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated date);"

    sql_fix: str = "CREATE TABLE tbl (\n    activated_date date\n);\n"

    date_column_without_suffix.config.lint.fix = True

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_non_applicable_fix_date_column_without_suffix(
    lint_date_column_without_suffix: core.Linter,
    date_column_without_suffix: core.BaseChecker,
) -> None:
    """Test fail fix date column without suffix."""
    sql_fail: str = """
    -- noqa: NM016
    CREATE TABLE tbl (activated date);
    """

    date_column_without_suffix.config.lint.fix = True

    violations: core.ViolationMetric = lint_date_column_without_suffix.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


@pytest.fixture(scope="module")
def single_letter_identifier() -> core.BaseChecker:
    """Create an instance of single letter identifier."""
    core.add_set_locations_to_rule(SingleLetterIdentifier)
    return SingleLetterIdentifier()


@pytest.fixture
def lint_single_letter_identifier(
    linter: core.Linter,
    single_letter_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint single letter identifier."""
    linter.checkers.add(single_letter_identifier)

    return linter


def test_fail_single_letter_identifier(
    lint_single_letter_identifier: core.Linter,
) -> None:
    """Test fail single letter identifier."""
    sql_fail: str = "CREATE TABLE tbl (a int);"

    violations: core.ViolationMetric = lint_single_letter_identifier.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_parse_error(lint_single_letter_identifier: core.Linter) -> None:
    """Test parse error."""
    source_code: str = """
    CREATE TABLE tbl (activated);
    """

    with pytest.raises(SystemExit) as excinfo:
        lint_single_letter_identifier.run(
            source_file=TEST_FILE,
            source_code=source_code,
        )

    assert excinfo.value.code == 1
