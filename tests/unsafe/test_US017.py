"""Test index movement to tablespace."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US017 import IndexMovementToTablespace


@pytest.fixture(scope="module")
def index_movement_to_tablespace() -> core.BaseChecker:
    """Create an instance of IndexMovementToTablespace."""
    core.add_set_locations_to_rule(IndexMovementToTablespace)
    return IndexMovementToTablespace()


@pytest.fixture
def lint_index_movement_to_tablespace(
    linter: core.Linter,
    index_movement_to_tablespace: core.BaseChecker,
) -> core.Linter:
    """Lint IndexMovementToTablespace."""
    linter.checkers.add(index_movement_to_tablespace)

    return linter


def test_index_movement_to_tablespace_rule_code(
    index_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test index movement to tablespace rule code."""
    assert (
        index_movement_to_tablespace.code
        == index_movement_to_tablespace.__module__.split(
            ".",
        )[-1]
    )


def test_index_movement_to_tablespace_auto_fixable(
    index_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test index movement to tablespace auto fixable."""
    assert index_movement_to_tablespace.is_auto_fixable is False


def test_fail_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test index movement to tablespace."""
    sql_fail: str = "ALTER INDEX public.idx SET TABLESPACE test;"

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        source_file=TEST_FILE,
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
    index_movement_to_tablespace: core.BaseChecker,
) -> None:
    """Test index movement to tablespace description."""
    sql_fail: str = "ALTER INDEX public.idx SET TABLESPACE test;"

    _: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(index_movement_to_tablespace.violations),
        ).description
        == "Index movement to tablespace"
    )


def test_pass_noqa_index_movement_to_tablespace(
    lint_index_movement_to_tablespace: core.Linter,
) -> None:
    """Test pass noqa index movement to tablespace."""
    sql_pass_noqa: str = """
    -- noqa: US017
    ALTER INDEX public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        source_file=TEST_FILE,
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
    """Test fail noqa index movement to tablespace."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER INDEX public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        source_file=TEST_FILE,
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
    """Test pass noqa index movement to tablespace."""
    sql_noqa: str = """
    -- noqa
    ALTER INDEX public.idx SET TABLESPACE test;
    """

    violations: core.ViolationMetric = lint_index_movement_to_tablespace.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
