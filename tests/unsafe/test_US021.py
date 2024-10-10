"""Test drop table."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US021 import DropTable


@pytest.fixture(scope="module")
def drop_table() -> core.BaseChecker:
    """Create an instance of DropTable."""
    core.add_set_locations_to_rule(DropTable)
    return DropTable()


@pytest.fixture
def lint_drop_table(
    linter: core.Linter,
    drop_table: core.BaseChecker,
) -> core.Linter:
    """Lint DropTable."""
    linter.checkers.add(drop_table)

    return linter


def test_drop_table_rule_code(
    drop_table: core.BaseChecker,
) -> None:
    """Test drop table rule code."""
    assert (
        drop_table.code
        == drop_table.__module__.split(
            ".",
        )[-1]
    )


def test_drop_table_auto_fixable(
    drop_table: core.BaseChecker,
) -> None:
    """Test drop table auto fixable."""
    assert drop_table.is_auto_fixable is False


def test_fail_drop_table(
    lint_drop_table: core.Linter,
) -> None:
    """Test drop table."""
    sql_fail: str = "DROP TABLE public.card;"

    violations: core.ViolationMetric = lint_drop_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_table_description(
    lint_drop_table: core.Linter,
    drop_table: core.BaseChecker,
) -> None:
    """Test drop table description."""
    sql_fail: str = "DROP TABLE public.card;"

    _: core.ViolationMetric = lint_drop_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(drop_table.violations),
        ).description
        == "Drop table found"
    )


def test_pass_noqa_drop_table(
    lint_drop_table: core.Linter,
) -> None:
    """Test pass noqa drop table."""
    sql_pass_noqa: str = """
    -- noqa: US021
    DROP TABLE public.card;
    """

    violations: core.ViolationMetric = lint_drop_table.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_table(
    lint_drop_table: core.Linter,
) -> None:
    """Test fail noqa drop table."""
    sql_noqa: str = """
    -- noqa: US001
    DROP TABLE public.card;
    """

    violations: core.ViolationMetric = lint_drop_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_drop_table(
    lint_drop_table: core.Linter,
) -> None:
    """Test pass noqa drop table."""
    sql_noqa: str = """
    -- noqa:
    DROP TABLE public.card;
    """

    violations: core.ViolationMetric = lint_drop_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
