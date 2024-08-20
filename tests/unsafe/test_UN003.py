"""Test column rename."""

import pytest

from pgshield import core
from pgshield.rules.unsafe.UN003 import ColumnRename


@pytest.fixture(scope="module")
def column_rename() -> core.Checker:
    """Create an instance of ColumnRename."""
    return ColumnRename()


@pytest.fixture()
def lint_column_rename(linter: core.Linter, column_rename: core.Checker) -> core.Linter:
    """Lint ColumnRename."""
    linter.checkers.add(column_rename)

    return linter


def test_column_rename_rule_code(column_rename: core.Checker) -> None:
    """Test column rename rule code."""
    assert column_rename.code == column_rename.__module__.split(".")[-1]


def test_column_rename_auto_fixable(column_rename: core.Checker) -> None:
    """Test column rename auto fixable."""
    assert column_rename.is_auto_fixable is False


def test_fail_column_rename(lint_column_rename: core.Linter) -> None:
    """Test fail column rename."""
    sql_fail: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id
    ;
    """

    violations: core.ViolationMetric = lint_column_rename.run(
        source_path="test.sql",
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_column_rename_description(
    lint_column_rename: core.Linter,
    column_rename: core.Checker,
) -> None:
    """Test fail column rename description."""
    sql_fail: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id
    ;
    """

    _: core.ViolationMetric = lint_column_rename.run(
        source_path="test.sql",
        source_code=sql_fail,
    )

    assert next(iter(column_rename.violations)).description == "Forbid column rename"


def test_pass_noqa_column_rename(lint_column_rename: core.Linter) -> None:
    """Test pass noqa column rename."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id -- noqa: UN003
    ;
    """

    violations: core.ViolationMetric = lint_column_rename.run(
        source_path="test.sql",
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_column_rename(lint_column_rename: core.Linter) -> None:
    """Test fail noqa column rename."""
    sql_noqa: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id -- noqa: UN002
    ;
    """

    violations: core.ViolationMetric = lint_column_rename.run(
        source_path="test.sql",
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_column_rename(
    lint_column_rename: core.Linter,
) -> None:
    """Test fail noqa column rename."""
    sql_noqa: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_column_rename.run(
        source_path="test.sql",
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
