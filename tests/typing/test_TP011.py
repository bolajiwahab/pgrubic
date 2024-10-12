"""Test usage of pg_float."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP011 import Float


@pytest.fixture(scope="module")
def pg_float() -> core.BaseChecker:
    """Create an instance of pg_float."""
    core.add_apply_fix_to_rule(Float)
    core.add_set_locations_to_rule(Float)
    return Float()


@pytest.fixture
def lint_float(
    linter: core.Linter,
    pg_float: core.BaseChecker,
) -> core.Linter:
    """Lint pg_float."""
    pg_float.config.lint.fix = False
    linter.checkers.add(pg_float)

    return linter


def test_float_rule_code(
    pg_float: core.BaseChecker,
) -> None:
    """Test pg_float rule code."""
    assert pg_float.code == pg_float.__module__.split(".")[-1]


def test_float_auto_fixable(
    pg_float: core.BaseChecker,
) -> None:
    """Test pg_float auto fixable."""
    assert pg_float.is_auto_fixable is True


def test_pass_create_table_numeric(
    lint_float: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = "CREATE TABLE tbl (retry_count numeric);"

    violations: core.ViolationMetric = lint_float.run(
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
    lint_float: core.Linter,
) -> None:
    """Test pass numeric."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN retry_count numeric;
    """

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_float(
    lint_float: core.Linter,
) -> None:
    """Test fail create table float."""
    sql_fail: str = "CREATE TABLE tbl (retry_count float);"

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_float(
    lint_float: core.Linter,
) -> None:
    """Test fail alter table float."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count float;"

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_float_description(
    lint_float: core.Linter,
    pg_float: core.BaseChecker,
) -> None:
    """Test float description."""
    sql_fail: str = "CREATE TABLE tbl (retry_count float);"

    _: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(pg_float.violations),
        ).description
        == "Prefer numeric over float"
    )


def test_pass_noqa_float(
    lint_float: core.Linter,
) -> None:
    """Test pass noqa float."""
    sql_pass_noqa: str = """
    -- noqa: TP011
    CREATE TABLE tbl (tbl_id int, retry_count float)
    """

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_float(
    lint_float: core.Linter,
) -> None:
    """Test fail noqa float."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN retry_count double precision;
    """

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_float(
    lint_float: core.Linter,
) -> None:
    """Test pass noqa float."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (tbl_id int, retry_count float);
    """

    violations: core.ViolationMetric = lint_float.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_float(
    lint_float: core.Linter,
    pg_float: core.BaseChecker,
) -> None:
    """Test fail fix float."""
    sql_fail: str = "CREATE TABLE tbl (user_id uuid, retry_count float);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id uuid\n  , retry_count numeric\n);"

    pg_float.config.lint.fix = True

    violations: core.ViolationMetric = lint_float.run(
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


def test_fail_fix_alter_table_float(
    lint_float: core.Linter,
    pg_float: core.BaseChecker,
) -> None:
    """Test fail fix float."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count double precision;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN retry_count numeric;"

    pg_float.config.lint.fix = True

    violations: core.ViolationMetric = lint_float.run(
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
