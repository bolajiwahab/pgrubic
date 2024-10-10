"""Test rename table."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US022 import RenameTable


@pytest.fixture(scope="module")
def rename_table() -> core.BaseChecker:
    """Create an instance of RenameTable."""
    core.add_set_locations_to_rule(RenameTable)
    return RenameTable()


@pytest.fixture
def lint_rename_table(
    linter: core.Linter,
    rename_table: core.BaseChecker,
) -> core.Linter:
    """Lint RenameTable."""
    linter.checkers.add(rename_table)

    return linter


def test_rename_table_rule_code(
    rename_table: core.BaseChecker,
) -> None:
    """Test rename table rule code."""
    assert (
        rename_table.code
        == rename_table.__module__.split(
            ".",
        )[-1]
    )


def test_rename_table_auto_fixable(
    rename_table: core.BaseChecker,
) -> None:
    """Test rename table auto fixable."""
    assert rename_table.is_auto_fixable is False


def test_fail_rename_table(
    lint_rename_table: core.Linter,
) -> None:
    """Test rename table."""
    sql_fail: str = "ALTER TABLE public.card RENAME TO card_old;"

    violations: core.ViolationMetric = lint_rename_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_rename_table_description(
    lint_rename_table: core.Linter,
    rename_table: core.BaseChecker,
) -> None:
    """Test rename table description."""
    sql_fail: str = "ALTER TABLE public.card RENAME TO card_old;"

    _: core.ViolationMetric = lint_rename_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(rename_table.violations),
        ).description
        == "Rename table detected"
    )


def test_pass_noqa_rename_table(
    lint_rename_table: core.Linter,
) -> None:
    """Test pass noqa rename table."""
    sql_pass_noqa: str = """
    -- noqa: US022
    ALTER TABLE public.card RENAME TO card_old;
    """

    violations: core.ViolationMetric = lint_rename_table.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_rename_table(
    lint_rename_table: core.Linter,
) -> None:
    """Test fail noqa rename table."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE public.card RENAME TO card_old;
    """

    violations: core.ViolationMetric = lint_rename_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_rename_table(
    lint_rename_table: core.Linter,
) -> None:
    """Test pass noqa rename table."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE public.card RENAME TO card_old;
    """

    violations: core.ViolationMetric = lint_rename_table.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
