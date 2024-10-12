"""Test table movement to tablespace."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US023 import TableMovementToTablespace


@pytest.fixture(scope="module")
def table_movement_to_tablespace() -> core.BaseChecker:
    """Create an instance of TableMovementToTablespace."""
    core.add_set_locations_to_rule(TableMovementToTablespace)
    return TableMovementToTablespace()


@pytest.fixture
def lint_index_movement_to_tablespace(
    linter: core.Linter,
    table_movement_to_tablespace: core.BaseChecker,
) -> core.Linter:
    """Lint TableMovementToTablespace."""
    linter.checkers.add(table_movement_to_tablespace)

    return linter


def test_index_movement_to_tablespace_rule_code(
    table_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test table movement to tablespace rule code."""
    assert (
        table_movement_to_tablespace.code
        == table_movement_to_tablespace.__module__.split(
            ".",
        )[-1]
    )


def test_index_movement_to_tablespace_auto_fixable(
    table_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test table movement to tablespace auto fixable."""
    assert table_movement_to_tablespace.is_auto_fixable is False


def test_fail_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test table movement to tablespace."""
    sql_fail: str = "ALTER TABLE public.idx SET TABLESPACE test;"

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_index_movement_to_tablespace_description(
    lint_index_movement_to_tablespace: core.Linter,
    table_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test table movement to tablespace description."""
    sql_fail: str = "ALTER TABLE public.idx SET TABLESPACE test;"

    _: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(table_movement_to_tablespace.violations),
        ).description
        == "Table movement to tablespace"
    )


def test_pass_noqa_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa table movement to tablespace."""
    sql_pass_noqa: str = """
    -- noqa: US023
    ALTER TABLE public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test fail noqa table movement to tablespace."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa table movement to tablespace."""
    sql_noqa: str = """
    -- noqa
    ALTER TABLE public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
