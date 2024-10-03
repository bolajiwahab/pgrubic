"""Test usage of disallowed data type."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.typing.TP014 import DisallowedDataType


@pytest.fixture(scope="module")
def disallowed_data_type() -> core.BaseChecker:
    """Create an instance of disallowed data type."""
    core.add_apply_fix_to_rule(DisallowedDataType)
    core.add_set_locations_to_rule(DisallowedDataType)
    return DisallowedDataType()


@pytest.fixture
def lint_disallowed_data_type(
    linter: core.Linter,
    disallowed_data_type: core.BaseChecker,
) -> core.Linter:
    """Lint disallowed data type."""
    disallowed_data_type.config.lint.fix = False
    disallowed_data_type.config.lint.disallowed_data_types = [
        config.DisallowedType(
            name="varchar",
            reason="deprecated",
            use_instead="text",
        ),
    ]
    linter.checkers.add(disallowed_data_type)

    return linter


def test_disallowed_data_type_rule_code(
    disallowed_data_type: core.BaseChecker,
) -> None:
    """Test disallowed data type rule code."""
    assert disallowed_data_type.code == disallowed_data_type.__module__.split(".")[-1]


def test_disallowed_data_type_auto_fixable(
    disallowed_data_type: core.BaseChecker,
) -> None:
    """Test disallowed data type auto fixable."""
    assert disallowed_data_type.is_auto_fixable is True


def test_pass_create_table_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test pass text."""
    sql_fail: str = "CREATE TABLE tbl (details text);"

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_disallowed_data_typeb(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test pass text."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN details text;
    """

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test fail create table disallowed data type."""
    sql_fail: str = "CREATE TABLE tbl (details varchar);"

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test fail alter table disallowed data type."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details varchar;"

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_disallowed_data_type_description(
    lint_disallowed_data_type: core.Linter,
    disallowed_data_type: core.BaseChecker,
) -> None:
    """Test disallowed data type description."""
    sql_fail: str = "CREATE TABLE tbl (details varchar);"

    _: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(disallowed_data_type.violations),
        ).description
        == "Data type 'varchar' is disallowed in config with reason: 'deprecated', use 'text' instead"  # noqa: E501
    )


def test_pass_noqa_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test pass noqa disallowed data type."""
    sql_pass_noqa: str = """
    -- noqa: TP014
    CREATE TABLE tbl (tbl_id int, details varchar)
    """

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test fail noqa disallowed data type."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN details varchar;
    """

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
) -> None:
    """Test pass noqa disallowed data type."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id int, details varchar);
    """

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
    disallowed_data_type: core.BaseChecker,
) -> None:
    """Test fail fix disallowed data type."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, details varchar);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id integer\n  , details text\n);"

    disallowed_data_type.config.lint.fix = True

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
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


def test_fail_fix_alter_table_disallowed_data_type(
    lint_disallowed_data_type: core.Linter,
    disallowed_data_type: core.BaseChecker,
) -> None:
    """Test fail fix disallowed data type."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details varchar;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN details text;"

    disallowed_data_type.config.lint.fix = True

    violations: core.ViolationMetric = lint_disallowed_data_type.run(
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
