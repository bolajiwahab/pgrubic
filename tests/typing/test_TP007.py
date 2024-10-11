"""Test usage of serial."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP007 import Serial


@pytest.fixture(scope="module")
def serial() -> core.BaseChecker:
    """Create an instance of serial."""
    core.add_apply_fix_to_rule(Serial)
    core.add_set_locations_to_rule(Serial)
    return Serial()


@pytest.fixture
def lint_serial(
    linter: core.Linter,
    serial: core.BaseChecker,
) -> core.Linter:
    """Lint serial."""
    serial.config.lint.fix = False
    linter.checkers.add(serial)

    return linter


def test_serial_rule_code(
    serial: core.BaseChecker,
) -> None:
    """Test serial rule code."""
    assert serial.code == serial.__module__.split(".")[-1]


def test_serial_auto_fixable(
    serial: core.BaseChecker,
) -> None:
    """Test serial auto fixable."""
    assert serial.is_auto_fixable is True


def test_pass_create_table_numeric(
    lint_serial: core.Linter,
) -> None:
    """Test pass identity column."""
    sql_fail: str = "CREATE TABLE tbl (tbl_id bigint GENERATED ALWAYS AS IDENTITY);"

    violations: core.ViolationMetric = lint_serial.run(
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
    lint_serial: core.Linter,
) -> None:
    """Test pass identity column."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN tbl_id bigint GENERATED ALWAYS AS IDENTITY;
    """

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_serial(
    lint_serial: core.Linter,
) -> None:
    """Test fail create table serial."""
    sql_fail: str = "CREATE TABLE tbl (tbl_id serial);"

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_smallserial(
    lint_serial: core.Linter,
) -> None:
    """Test fail alter table smallserial."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN tbl_id smallserial;"

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_serial_description(
    lint_serial: core.Linter,
    serial: core.BaseChecker,
) -> None:
    """Test serial description."""
    sql_fail: str = "CREATE TABLE tbl (tbl_id bigserial);"

    _: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(serial.violations),
        ).description
        == "Prefer identity column over serial types"
    )


def test_pass_noqa_serial(
    lint_serial: core.Linter,
) -> None:
    """Test pass noqa serial."""
    sql_pass_noqa: str = """
    -- noqa: TP007
    CREATE TABLE tbl (tbl_id int, tbl_id serial)
    """

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_serial(
    lint_serial: core.Linter,
) -> None:
    """Test fail noqa serial."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN tbl_id bigserial;
    """

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_serial(
    lint_serial: core.Linter,
) -> None:
    """Test pass noqa serial."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id int, tbl_id smallserial);
    """

    violations: core.ViolationMetric = lint_serial.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_serial(
    lint_serial: core.Linter,
    serial: core.BaseChecker,
) -> None:
    """Test fail fix serial."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, tbl_id serial);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id integer\n  , tbl_id bigint GENERATED ALWAYS AS IDENTITY \n);"  # noqa: E501

    serial.config.lint.fix = True

    violations: core.ViolationMetric = lint_serial.run(
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


def test_fail_fix_alter_table_serial(
    lint_serial: core.Linter,
    serial: core.BaseChecker,
) -> None:
    """Test fail fix serial."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN total serial;"

    sql_fix: str = (
        "ALTER TABLE tbl\n    ADD COLUMN total bigint GENERATED ALWAYS AS IDENTITY ;"
    )

    serial.config.lint.fix = True

    violations: core.ViolationMetric = lint_serial.run(
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
