"""Test invalid index name."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM001 import InvalidIndexName


@pytest.fixture(scope="module")
def invalid_index_name() -> core.BaseChecker:
    """Create an instance of invalid index name."""
    core.add_set_locations_to_rule(InvalidIndexName)
    return InvalidIndexName()


@pytest.fixture
def lint_invalid_index_name(
    linter: core.Linter,
    invalid_index_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid index name."""
    invalid_index_name.config.lint.regex_index = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_idx$"
    )

    linter.checkers.add(invalid_index_name)

    return linter


def test_invalid_index_name_rule_code(
    invalid_index_name: core.BaseChecker,
) -> None:
    """Test invalid index name rule code."""
    assert invalid_index_name.code == invalid_index_name.__module__.split(".")[-1]


def test_invalid_index_name_auto_fixable(
    invalid_index_name: core.BaseChecker,
) -> None:
    """Test invalid index name auto fixable."""
    assert invalid_index_name.is_auto_fixable is False


def test_pass_implicit_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test pass implicit index name."""
    sql_pass: str = "CREATE INDEX ON tbl (col);"

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test pass valid index name."""
    sql_fail: str = "CREATE INDEX tbl_col_idx ON tbl (col);"

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test fail invalid index name."""
    sql_fail: str = "CREATE INDEX col_idx ON tbl (col);"

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_index_name_description(
    lint_invalid_index_name: core.Linter,
    invalid_index_name: core.BaseChecker,
) -> None:
    """Test invalid index name description."""
    sql_fail: str = "CREATE INDEX idx ON tbl (col);"

    _: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_index_name.violations),
        ).description
        == f"Index `idx` does not follow naming convention `{invalid_index_name.config.lint.regex_index}`"  # noqa: E501
    )


def test_pass_noqa_invalid_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test pass noqa invalid index name."""
    sql_pass_noqa: str = """
    -- noqa: NM001
    CREATE INDEX idx ON tbl (col);
    """

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test fail noqa invalid index name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE INDEX idx ON tbl (col);
    """

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_index_name(
    lint_invalid_index_name: core.Linter,
) -> None:
    """Test pass noqa invalid index name."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE INDEX idx ON tbl (col);
    """

    violations: core.ViolationMetric = lint_invalid_index_name.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
