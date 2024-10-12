"""Test usage of smallint."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP010 import Smallint


@pytest.fixture(scope="module")
def smallint() -> core.BaseChecker:
    """Create an instance of smallint."""
    core.add_apply_fix_to_rule(Smallint)
    core.add_set_locations_to_rule(Smallint)
    return Smallint()


@pytest.fixture
def lint_smallint(
    linter: core.Linter,
    smallint: core.BaseChecker,
) -> core.Linter:
    """Lint smallint."""
    smallint.config.lint.fix = False
    linter.checkers.add(smallint)

    return linter


def test_smallint_rule_code(
    smallint: core.BaseChecker,
) -> None:
    """Test smallint rule code."""
    assert smallint.code == smallint.__module__.split(".")[-1]


def test_smallint_auto_fixable(
    smallint: core.BaseChecker,
) -> None:
    """Test smallint auto fixable."""
    assert smallint.is_auto_fixable is True


def test_pass_create_table_bigint(
    lint_smallint: core.Linter,
) -> None:
    """Test pass bigint."""
    sql_fail: str = "CREATE TABLE tbl (retry_count bigint);"

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_bigint(
    lint_smallint: core.Linter,
) -> None:
    """Test pass bigint."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN retry_count bigint;
    """

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_smallint(
    lint_smallint: core.Linter,
) -> None:
    """Test fail create table smallint."""
    sql_fail: str = "CREATE TABLE tbl (retry_count smallint);"

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_smallint(
    lint_smallint: core.Linter,
) -> None:
    """Test fail alter table smallint."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count smallint;"

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_smallint_description(
    lint_smallint: core.Linter,
    smallint: core.BaseChecker,
) -> None:
    """Test smallint description."""
    sql_fail: str = "CREATE TABLE tbl (retry_count smallint);"

    _: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(smallint.violations),
        ).description
        == "Prefer bigint over smallint"
    )


def test_pass_noqa_smallint(
    lint_smallint: core.Linter,
) -> None:
    """Test pass noqa smallint."""
    sql_pass_noqa: str = """
    -- noqa: TP010
    CREATE TABLE tbl (tbl_id int, retry_count smallint)
    """

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_smallint(
    lint_smallint: core.Linter,
) -> None:
    """Test fail noqa smallint."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN retry_count smallint;
    """

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_smallint(
    lint_smallint: core.Linter,
) -> None:
    """Test pass noqa smallint."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (tbl_id int, retry_count smallint);
    """

    violations: core.ViolationMetric = lint_smallint.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_smallint(
    lint_smallint: core.Linter,
    smallint: core.BaseChecker,
) -> None:
    """Test fail fix smallint."""
    sql_fail: str = "CREATE TABLE tbl (user_id uuid, retry_count smallint);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id uuid\n  , retry_count bigint\n);"

    smallint.config.lint.fix = True

    violations: core.ViolationMetric = lint_smallint.run(
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


def test_fail_fix_alter_table_smallint(
    lint_smallint: core.Linter,
    smallint: core.BaseChecker,
) -> None:
    """Test fail fix smallint."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count smallint;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN retry_count bigint;"

    smallint.config.lint.fix = True

    violations: core.ViolationMetric = lint_smallint.run(
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
