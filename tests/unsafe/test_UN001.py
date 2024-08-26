"""Test drop column."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.UN001 import DropColumn


@pytest.fixture(scope="module")
def drop_column() -> core.BaseChecker:
    """Create an instance of DropColumn."""
    return DropColumn()


@pytest.fixture
def lint_drop_column(linter: core.Linter, drop_column: core.BaseChecker) -> core.Linter:
    """Lint DropColumn."""
    linter.checkers.add(drop_column)

    return linter


def test_drop_column_rule_code(drop_column: core.BaseChecker) -> None:
    """Test drop column rule code."""
    assert drop_column.code == drop_column.__module__.split(".")[-1]


def test_drop_column_auto_fixable(drop_column: core.BaseChecker) -> None:
    """Test drop column auto fixable."""
    assert drop_column.is_auto_fixable is False


def test_fail_drop_column(lint_drop_column: core.Linter) -> None:
    """Test fail drop column."""
    sql_fail: str = """
    ALTER TABLE public.card DROP COLUMN id
    ;
    """

    violations: core.ViolationMetric = lint_drop_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_column_description(
    lint_drop_column: core.Linter,
    drop_column: core.BaseChecker,
) -> None:
    """Test fail drop column description."""
    sql_fail: str = """
    ALTER TABLE public.card DROP COLUMN id
    ;
    """

    _: core.ViolationMetric = lint_drop_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert next(iter(drop_column.violations)).description == "Drop column detected"


def test_pass_noqa_drop_column(lint_drop_column: core.Linter) -> None:
    """Test pass noqa drop column."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card DROP COLUMN id -- noqa: UN001
    ;
    """

    violations: core.ViolationMetric = lint_drop_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_column(lint_drop_column: core.Linter) -> None:
    """Test fail noqa drop column."""
    sql_noqa: str = """
    ALTER TABLE public.card DROP COLUMN id -- noqa: UN002
    ;
    """

    violations: core.ViolationMetric = lint_drop_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_drop_column(
    lint_drop_column: core.Linter,
) -> None:
    """Test fail noqa drop column."""
    sql_noqa: str = """
    ALTER TABLE public.card DROP COLUMN id -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_drop_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
