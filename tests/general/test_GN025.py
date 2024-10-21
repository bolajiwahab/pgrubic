"""Test duplicate index."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN025 import DuplicateIndex


@pytest.fixture(scope="module")
def duplicate_index() -> core.BaseChecker:
    """Create an instance of DuplicateIndex."""
    core.add_set_locations_to_rule(DuplicateIndex)
    return DuplicateIndex()


@pytest.fixture
def lint_duplicate_index(
    linter: core.Linter,
    duplicate_index: core.BaseChecker,
) -> core.Linter:
    """Lint DuplicateIndex."""
    linter.checkers.add(duplicate_index)

    return linter


def test_duplicate_index_rule_code(
    duplicate_index: core.BaseChecker,
) -> None:
    """Test duplicate index rule code."""
    assert duplicate_index.code == duplicate_index.__module__.split(".")[-1]


def test_duplicate_index_auto_fixable(
    duplicate_index: core.BaseChecker,
) -> None:
    """Test duplicate index auto fixable."""
    assert duplicate_index.is_auto_fixable is False


def test_pass_named_indexes_no_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test pass no duplicate index."""
    sql_pass: str = """
    CREATE INDEX idx_city_id ON measurement (city_id);
    CREATE INDEX idx_logdate ON measurement (logdate);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_unnamed_indexes_no_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test pass unnamed indexes no duplicate index."""
    sql_pass: str = """
    CREATE INDEX ON measurement (country_id);
    CREATE INDEX ON measurement (created_date);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_mixed_columns_no_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test pass mixed columns indexes."""
    sql_pass: str = """
    CREATE INDEX city_id_logdate_idx ON measurement (city_id, logdate);
    CREATE INDEX logdate_city_id_idx ON measurement (logdate, city_id);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test fail duplicate index."""
    sql_fail: str = """
    CREATE INDEX ON measurement (log_date);
    CREATE UNIQUE INDEX ON measurement (log_date);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_duplicate_index_description(
    lint_duplicate_index: core.Linter,
    duplicate_index: core.BaseChecker,
) -> None:
    """Test duplicate index description."""
    sql_fail: str = """
    CREATE INDEX ON measurement (logdate, city_id);
    CREATE INDEX ON measurement (logdate, city_id);
    """

    _: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(duplicate_index.violations),
        ).description
        == "Duplicate index detected"
    )


def test_pass_noqa_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test pass noqa duplicate index."""
    sql_pass_noqa: str = """
    CREATE INDEX ON measurement (created_at, city_id);
    -- noqa: GN025
    CREATE INDEX ON measurement (created_at, city_id);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test fail noqa duplicate index."""
    sql_fail_noqa: str = """
    CREATE INDEX ON measurement (created_date, city_id);
    -- noqa: GN001
    CREATE INDEX ON measurement (created_date, city_id);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_duplicate_index(
    lint_duplicate_index: core.Linter,
) -> None:
    """Test pass general noqa duplicate index."""
    sql_pass_noqa: str = """
    CREATE INDEX ON measurement (id, city_id);
    -- noqa
    CREATE INDEX ON measurement (id, city_id);
    """

    violations: core.ViolationMetric = lint_duplicate_index.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
