"""Test usage of numeric with precision."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP016 import NumericWithPrecision


@pytest.fixture(scope="module")
def numeric_with_precision() -> core.BaseChecker:
    """Create an instance of numeric with precision."""
    core.add_apply_fix_to_rule(NumericWithPrecision)
    core.add_set_locations_to_rule(NumericWithPrecision)
    return NumericWithPrecision()


@pytest.fixture
def lint_numeric_with_precision(
    linter: core.Linter,
    numeric_with_precision: core.BaseChecker,
) -> core.Linter:
    """Lint numeric with precision."""
    numeric_with_precision.config.lint.fix = False
    linter.checkers.add(numeric_with_precision)

    return linter


def test_numeric_with_precision_rule_code(
    numeric_with_precision: core.BaseChecker,
) -> None:
    """Test numeric with precision rule code."""
    assert numeric_with_precision.code == numeric_with_precision.__module__.split(".")[-1]


def test_numeric_with_precision_auto_fixable(
    numeric_with_precision: core.BaseChecker,
) -> None:
    """Test numeric with precision auto fixable."""
    assert numeric_with_precision.is_auto_fixable is True


def test_pass_create_table_numeric(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = "CREATE TABLE transaction (amount numeric);"

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_numeric(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN amount numeric;"

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test fail create table numeric with precision."""
    sql_fail: str = "CREATE TABLE transaction (amount numeric(9, 2));"

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test fail alter table numeric with precision."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN amount numeric(9, 2);"

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_numeric_with_precision_description(
    lint_numeric_with_precision: core.Linter,
    numeric_with_precision: core.BaseChecker,
) -> None:
    """Test numeric with precision description."""
    sql_fail: str = "CREATE TABLE transaction (amount numeric(9, 2));"

    _: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(numeric_with_precision.violations),
        ).description
        == "Prefer entire numeric"
    )


def test_pass_noqa_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test pass noqa numeric with precision."""
    sql_pass_noqa: str = """
    -- noqa: TP016
    CREATE TABLE transaction (transaction_id int, amount numeric(9, 2))
    """

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test fail noqa numeric with precision."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE transaction ADD COLUMN amount numeric(9, 2);
    """

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
) -> None:
    """Test pass noqa numeric with precision."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE transaction (transaction_id int, amount numeric(9, 2));
    """

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
    numeric_with_precision: core.BaseChecker,
) -> None:
    """Test fail fix numeric with precision."""
    sql_fail: str = "CREATE TABLE transaction (user_id int, amount numeric(9, 2));"

    sql_fix: str = (
        "CREATE TABLE transaction (\n    user_id integer\n  , amount numeric\n);"
    )

    numeric_with_precision.config.lint.fix = True

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_numeric_with_precision(
    lint_numeric_with_precision: core.Linter,
    numeric_with_precision: core.BaseChecker,
) -> None:
    """Test fail fix numeric with precision."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN total numeric(9, 2);"

    sql_fix: str = "ALTER TABLE transaction\n    ADD COLUMN total numeric;"

    numeric_with_precision.config.lint.fix = True

    violations: core.ViolationMetric = lint_numeric_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
