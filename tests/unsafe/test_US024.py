"""Test tables movement to tablespace."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US024 import TablesMovementToTablespace


@pytest.fixture(scope="module")
def tables_movement_to_tablespace() -> core.BaseChecker:
    """Create an instance of TablesMovementToTablespace."""
    core.add_set_locations_to_rule(TablesMovementToTablespace)
    return TablesMovementToTablespace()


@pytest.fixture
def lint_indexes_movement_to_tablespace(
    linter: core.Linter,
    tables_movement_to_tablespace: core.BaseChecker,
) -> core.Linter:
    """Lint TablesMovementToTablespace."""
    linter.checkers.add(tables_movement_to_tablespace)

    return linter


def test_indexes_movement_to_tablespace_rule_code(
    tables_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test tables movement to tablespace rule code."""
    assert (
        tables_movement_to_tablespace.code
        == tables_movement_to_tablespace.__module__.split(
            ".",
        )[-1]
    )


def test_indexes_movement_to_tablespace_auto_fixable(
    tables_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test tables movement to tablespace auto fixable."""
    assert tables_movement_to_tablespace.is_auto_fixable is False


def test_pass_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test tables movement to tablespace."""
    sql_fail: str = "ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test;"

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
    """Test tables movement to tablespace."""
    sql_fail: str = "ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test2;"

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
    tables_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test tables movement to tablespace description."""
    sql_fail: str = "ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test2;"

    _: core.ViolationMetric = lint_indexes_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(tables_movement_to_tablespace.violations),
        ).description
        == "Tables movement to tablespace"
    )


def test_pass_noqa_indexes_movement_to_tablespace(
    lint_indexes_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa tables movement to tablespace."""
    sql_pass_noqa: str = """
    -- noqa: US024
    ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test2;
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
    """Test fail noqa tables movement to tablespace."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test2;
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
    """Test pass noqa tables movement to tablespace."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE ALL IN TABLESPACE test SET TABLESPACE test;
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
