"""Test indexes movement to tablespace."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US018 import IndexesMovementToTablespace


@pytest.fixture(scope="module")
def indexes_movement_to_tablespace() -> core.BaseChecker:
    """Create an instance of IndexesMovementToTablespace."""
    core.add_set_locations_to_rule(IndexesMovementToTablespace)
    return IndexesMovementToTablespace()


@pytest.fixture
def lint_indexes_movement_to_tablespace(
    linter: core.Linter,
    indexes_movement_to_tablespace: core.BaseChecker,
) -> core.Linter:
    """Lint IndexesMovementToTablespace."""
    linter.checkers.add(indexes_movement_to_tablespace)

    return linter


def test_indexes_movement_to_tablespace_rule_code(
    indexes_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test indexes movement to tablespace rule code."""
    assert (
        indexes_movement_to_tablespace.code
        == indexes_movement_to_tablespace.__module__.split(
            ".",
        )[-1]
    )


def test_indexes_movement_to_tablespace_auto_fixable(
    indexes_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test indexes movement to tablespace auto fixable."""
    assert indexes_movement_to_tablespace.is_auto_fixable is False


def test_pass_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test indexes movement to tablespace."""
    sql_fail: str = "ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test;"

    violations: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test indexes movement to tablespace."""
    sql_fail: str = "ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test2;"

    violations: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_indexes_movement_to_tablespace_description(
    lint_indexes_movement_to_tablespace: core.Linter,
    indexes_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test indexes movement to tablespace description."""
    sql_fail: str = "ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test2;"

    _: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(indexes_movement_to_tablespace.violations),
        ).description
        == "Indexes movement to tablespace"
    )


def test_pass_noqa_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa indexes movement to tablespace."""
    sql_pass_noqa: str = """
    -- noqa: US018
    ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test2;
    """

    violations: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test fail noqa indexes movement to tablespace."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test2;
    """

    violations: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa indexes movement to tablespace."""
    sql_noqa: str = """
    -- noqa:
    ALTER INDEX ALL IN TABLESPACE test SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
