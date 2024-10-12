"""Test truncate table."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US029 import TruncateTable


@pytest.fixture(scope="module")
def truncate_table() -> core.BaseChecker:
    """Create an instance of TruncateTable."""
    core.add_set_locations_to_rule(TruncateTable)
    return TruncateTable()


@pytest.fixture
def lint_truncate_table(
    linter: core.Linter,
    truncate_table: core.BaseChecker,
) -> core.Linter:
    """Lint TruncateTable."""
    linter.checkers.add(truncate_table)

    return linter


def test_truncate_table_rule_code(
    truncate_table: core.BaseChecker,
) -> None:
    """Test truncate table rule code."""
    assert (
        truncate_table.code
        == truncate_table.__module__.split(
            ".",
        )[-1]
    )


def test_truncate_table_auto_fixable(
    truncate_table: core.BaseChecker,
) -> None:
    """Test truncate table auto fixable."""
    assert truncate_table.is_auto_fixable is False


def test_fail_truncate_table(
    lint_truncate_table: core.Linter,
) -> None:
    """Test truncate table."""
    sql_fail: str = "TRUNCATE TABLE public.card;"

    violations: core.ViolationMetric = lint_truncate_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_truncate_table_description(
    lint_truncate_table: core.Linter,
    truncate_table: core.BaseChecker,
) -> None:
    """Test truncate table description."""
    sql_fail: str = "TRUNCATE TABLE public.card;"

    _: core.ViolationMetric = lint_truncate_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(truncate_table.violations),
        ).description
        == "Truncate table detected"
    )


def test_pass_noqa_truncate_table(
    lint_truncate_table: core.Linter,
) -> None:
    """Test pass noqa truncate table."""
    sql_pass_noqa: str = """
    -- noqa: US029
    TRUNCATE TABLE public.card;
    """

    violations: core.ViolationMetric = lint_truncate_table.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_truncate_table(
    lint_truncate_table: core.Linter,
) -> None:
    """Test fail noqa truncate table."""
    sql_noqa: str = """
    -- noqa: US001
    TRUNCATE TABLE public.card;
    """

    violations: core.ViolationMetric = lint_truncate_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_truncate_table(
    lint_truncate_table: core.Linter,
) -> None:
    """Test pass noqa truncate table."""
    sql_noqa: str = """
    -- noqa
    TRUNCATE TABLE public.card;
    """

    violations: core.ViolationMetric = lint_truncate_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
