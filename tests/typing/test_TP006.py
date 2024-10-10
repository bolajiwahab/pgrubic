"""Test usage of money."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP006 import Money


@pytest.fixture(scope="module")
def money() -> core.BaseChecker:
    """Create an instance of money."""
    core.add_apply_fix_to_rule(Money)
    core.add_set_locations_to_rule(Money)
    return Money()


@pytest.fixture
def lint_money(
    linter: core.Linter,
    money: core.BaseChecker,
) -> core.Linter:
    """Lint money."""
    money.config.lint.fix = False
    linter.checkers.add(money)

    return linter


def test_money_rule_code(
    money: core.BaseChecker,
) -> None:
    """Test money rule code."""
    assert money.code == money.__module__.split(".")[-1]


def test_money_auto_fixable(
    money: core.BaseChecker,
) -> None:
    """Test money auto fixable."""
    assert money.is_auto_fixable is True


def test_pass_create_table_numeric(
    lint_money: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = "CREATE TABLE transaction (amount numeric);"

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_numeric(
    lint_money: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN amount numeric;"

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_money(
    lint_money: core.Linter,
) -> None:
    """Test fail create table money."""
    sql_fail: str = "CREATE TABLE transaction (amount money);"

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_money(
    lint_money: core.Linter,
) -> None:
    """Test fail alter table money."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN amount money;"

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_money_description(
    lint_money: core.Linter,
    money: core.BaseChecker,
) -> None:
    """Test money description."""
    sql_fail: str = "CREATE TABLE transaction (amount money);"

    _: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(money.violations),
        ).description
        == "Prefer numeric to money"
    )


def test_pass_noqa_money(
    lint_money: core.Linter,
) -> None:
    """Test pass noqa money."""
    sql_pass_noqa: str = """
    -- noqa: TP006
    CREATE TABLE transaction (transaction_id int, amount money)
    """

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_money(
    lint_money: core.Linter,
) -> None:
    """Test fail noqa money."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE transaction ADD COLUMN amount money;
    """

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_money(
    lint_money: core.Linter,
) -> None:
    """Test pass noqa money."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE transaction (transaction_id int, amount money);
    """

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_money(
    lint_money: core.Linter,
    money: core.BaseChecker,
) -> None:
    """Test fail fix money."""
    sql_fail: str = "CREATE TABLE transaction (user_id int, amount money);"

    sql_fix: str = (
        "CREATE TABLE transaction (\n    user_id integer\n  , amount numeric\n);"
    )

    money.config.lint.fix = True

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_money(
    lint_money: core.Linter,
    money: core.BaseChecker,
) -> None:
    """Test fail fix money."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN total money;"

    sql_fix: str = "ALTER TABLE transaction\n    ADD COLUMN total numeric;"

    money.config.lint.fix = True

    violations: core.ViolationMetric = lint_money.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
