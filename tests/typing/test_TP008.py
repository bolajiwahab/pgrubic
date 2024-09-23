"""Test for usage of json."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP008 import Json


@pytest.fixture(scope="module")
def json() -> core.BaseChecker:
    """Create an instance of json."""
    core.add_apply_fix_to_rule(Json)
    core.add_set_locations_to_rule(Json)
    return Json()


@pytest.fixture
def lint_json(
    linter: core.Linter,
    json: core.BaseChecker,
) -> core.Linter:
    """Lint json."""
    json.config.lint.fix = False
    linter.checkers.add(json)

    return linter


def test_json_rule_code(
    json: core.BaseChecker,
) -> None:
    """Test json rule code."""
    assert json.code == json.__module__.split(".")[-1]


def test_json_auto_fixable(
    json: core.BaseChecker,
) -> None:
    """Test json auto fixable."""
    assert json.is_auto_fixable is True


def test_pass_create_table_jsonb(
    lint_json: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = "CREATE TABLE tbl (details jsonb);"

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_jsonb(
    lint_json: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN details jsonb;
    """

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_json(
    lint_json: core.Linter,
) -> None:
    """Test fail create table json."""
    sql_fail: str = "CREATE TABLE tbl (details json);"

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_json(
    lint_json: core.Linter,
) -> None:
    """Test fail alter table json."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details json;"

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_json_description(
    lint_json: core.Linter,
    json: core.BaseChecker,
) -> None:
    """Test json description."""
    sql_fail: str = "CREATE TABLE tbl (details json);"

    _: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(json.violations),
        ).description
        == "Prefer jsonb over json"
    )


def test_pass_noqa_json(
    lint_json: core.Linter,
) -> None:
    """Test pass noqa json."""
    sql_pass_noqa: str = """
    -- noqa: TP008
    CREATE TABLE tbl (tbl_id int, details json)
    """

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_json(
    lint_json: core.Linter,
) -> None:
    """Test fail noqa json."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN details json;
    """

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_json(
    lint_json: core.Linter,
) -> None:
    """Test pass noqa json."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id int, details json);
    """

    violations: core.ViolationMetric = lint_json.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_json(
    lint_json: core.Linter,
    json: core.BaseChecker,
) -> None:
    """Test fail fix json."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, details json);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id integer\n  , details jsonb\n);"

    json.config.lint.fix = True

    violations: core.ViolationMetric = lint_json.run(
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


def test_fail_fix_alter_table_json(
    lint_json: core.Linter,
    json: core.BaseChecker,
) -> None:
    """Test fail fix json."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details json;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN details jsonb;"

    json.config.lint.fix = True

    violations: core.ViolationMetric = lint_json.run(
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
