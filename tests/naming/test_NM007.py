"""Test invalid sequence name."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM007 import InvalidSequenceName


@pytest.fixture(scope="module")
def invalid_sequence_name() -> core.BaseChecker:
    """Create an instance of invalid sequence name."""
    core.add_set_locations_to_rule(InvalidSequenceName)
    return InvalidSequenceName()


@pytest.fixture
def lint_invalid_sequence_name(
    linter: core.Linter,
    invalid_sequence_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid sequence name."""
    invalid_sequence_name.config.lint.regex_sequence = "[a-zA-Z0-9].+_seq$"

    linter.checkers.add(invalid_sequence_name)

    return linter


def test_invalid_sequence_name_rule_code(
    invalid_sequence_name: core.BaseChecker,
) -> None:
    """Test invalid sequence name rule code."""
    assert invalid_sequence_name.code == invalid_sequence_name.__module__.split(".")[-1]


def test_invalid_sequence_name_auto_fixable(
    invalid_sequence_name: core.BaseChecker,
) -> None:
    """Test invalid sequence name auto fixable."""
    assert invalid_sequence_name.is_auto_fixable is False


def test_pass_implicit_sequence_name_create_table(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test pass implicit sequence name."""
    sql_pass: str = "CREATE TABLE tbl (col serial);"

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_implicit_sequence_name_add_column(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test pass implicit sequence name."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN tbl_id serial;"

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_sequence_name(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test pass valid invalid sequence name."""
    sql_fail: str = "CREATE SEQUENCE tbl_col_seq START 101;"

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_sequence_name(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test fail invalid sequence name."""
    sql_fail: str = "CREATE SEQUENCE seq START 101;"

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_sequence_name_description(
    lint_invalid_sequence_name: core.Linter,
    invalid_sequence_name: core.BaseChecker,
) -> None:
    """Test invalid sequence name description."""
    sql_fail: str = "CREATE SEQUENCE seq START 101;"

    _: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_sequence_name.violations),
        ).description
        == f"Sequence `seq` does not follow naming convention `{invalid_sequence_name.config.lint.regex_sequence}`"  # noqa: E501
    )


def test_pass_noqa_invalid_sequence_name(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test pass noqa invalid sequence name."""
    sql_pass_noqa: str = """
    -- noqa: NM007
    CREATE SEQUENCE seq START 101;
    """

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_sequence_name(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test fail noqa invalid sequence name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE SEQUENCE seq START 101;
    """

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_sequence_name(
    lint_invalid_sequence_name: core.Linter,
) -> None:
    """Test pass noqa invalid sequence name."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE SEQUENCE seq START 101;
    """

    violations: core.ViolationMetric = lint_invalid_sequence_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
