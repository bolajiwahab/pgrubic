"""Test required column removal."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.general.GN012 import RequiredColumnRemoval


@pytest.fixture(scope="module")
def required_column_removal() -> core.BaseChecker:
    """Create an instance of RequiredColumnRemoval."""
    core.add_set_locations_to_rule(RequiredColumnRemoval)
    return RequiredColumnRemoval()


@pytest.fixture
def lint_required_column_removal(
    linter: core.Linter,
    required_column_removal: core.BaseChecker,
) -> core.Linter:
    """Lint RequiredColumnRemoval."""
    required_column_removal.config.lint.required_columns = [
        config.Column(
            name="created_at",
            data_type="timestamptz",
        ),
    ]
    linter.checkers.add(required_column_removal)

    return linter


def test_required_column_removal_rule_code(
    required_column_removal: core.BaseChecker,
) -> None:
    """Test required column removal rule code."""
    assert (
        required_column_removal.code == required_column_removal.__module__.split(".")[-1]
    )


def test_required_column_removal_auto_fixable(
    required_column_removal: core.BaseChecker,
) -> None:
    """Test required column removal auto fixable."""
    assert required_column_removal.is_auto_fixable is False


def test_pass_no_columns_table(
    lint_required_column_removal: core.Linter,
) -> None:
    """Test fail required column removal."""
    sql_fail: str = "ALTER TABLE music DROP COLUMN age;"

    violations: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_required_column_removal(
    lint_required_column_removal: core.Linter,
) -> None:
    """Test fail required column removal."""
    sql_fail: str = "ALTER TABLE music DROP COLUMN created_at;"

    violations: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_required_column_removal_description(
    lint_required_column_removal: core.Linter,
    required_column_removal: core.BaseChecker,
) -> None:
    """Test required column removal description."""
    sql_fail: str = "ALTER TABLE music DROP COLUMN created_at"

    _: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(required_column_removal.violations),
        ).description
        == "Column `created_at` is marked as required in config"
    )


def test_pass_noqa_required_column_removal(
    lint_required_column_removal: core.Linter,
) -> None:
    """Test pass noqa required column removal."""
    sql_pass_noqa: str = """
    -- noqa: GN012
    ALTER TABLE music DROP COLUMN created_at
    """

    violations: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_required_column_removal(
    lint_required_column_removal: core.Linter,
) -> None:
    """Test fail noqa required column removal."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE music DROP COLUMN created_at
    """

    violations: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_required_column_removal(
    lint_required_column_removal: core.Linter,
) -> None:
    """Test fail noqa required column removal."""
    sql_pass_noqa: str = """
    -- noqa:
    ALTER TABLE music DROP COLUMN created_at
    """

    violations: core.ViolationMetric = lint_required_column_removal.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
