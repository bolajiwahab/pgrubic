"""Test usage of disallowed schemas."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.schema.SM002 import DisallowedSchema


@pytest.fixture(scope="module")
def disallowed_schema() -> core.BaseChecker:
    """Create an instance of DisallowedSchema."""
    core.add_apply_fix_to_rule(DisallowedSchema)
    core.add_set_locations_to_rule(DisallowedSchema)
    return DisallowedSchema()


@pytest.fixture
def lint_disallowed_schema(
    linter: core.Linter,
    disallowed_schema: core.BaseChecker,
) -> core.Linter:
    """Lint DisallowedSchema."""
    disallowed_schema.config.lint.fix = False
    disallowed_schema.config.lint.disallowed_schemas = [
        config.DisallowedSchema(
            name="test",
            reason="test",
            use_instead="app",
        ),
    ]
    linter.checkers.add(disallowed_schema)

    return linter


def test_disallowed_schema_rule_code(
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test disallowed schema rule code."""
    assert disallowed_schema.code == disallowed_schema.__module__.split(".")[-1]


def test_disallowed_schema_auto_fixable(
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test disallowed schema auto fixable."""
    assert disallowed_schema.is_auto_fixable is True


def test_pass_no_explicit_schema(
    lint_disallowed_schema: core.Linter,
) -> None:
    """Test pass no explicit schema."""
    sql_fail: str = "CREATE TABLE card();"

    violations: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_explicit_not_disallowed_schema(
    lint_disallowed_schema: core.Linter,
) -> None:
    """Test pass explicit not disallowed schema."""
    sql_fail: str = "CREATE TABLE public.card();"

    violations: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_disallowed_schema_description(
    lint_disallowed_schema: core.Linter,
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test fail disallowed schema description."""
    sql_fail: str = "CREATE TABLE test.card();"

    _: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(disallowed_schema.violations)).description
        == "Schema 'test' is disallowed in config with reason: 'test', use 'app' instead"
    )


def test_fail_table_disallowed_schema(
    lint_disallowed_schema: core.Linter,
) -> None:
    """Test fail table disallowed schema."""
    sql_fail: str = "CREATE TABLE test.card();"

    violations: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_fix_table_disallowed_schema(
    lint_disallowed_schema: core.Linter,
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test fail fix table disallowed schema."""
    sql_fail: str = "CREATE TABLE test.card();"

    sql_fix: str = "CREATE TABLE app.card ();"

    disallowed_schema.config.lint.fix = True

    violations: core.ViolationMetric = lint_disallowed_schema.run(
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


def test_fail_function_disallowed_schema(
    lint_disallowed_schema: core.Linter,
) -> None:
    """Test fail function disallowed schema."""
    sql_fail: str = """
    CREATE FUNCTION test.dup(int) RETURNS TABLE(f1 int) LANGUAGE SQL
    AS $$ SELECT $1 $$
    ;
    """

    violations: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_fix_function_disallowed_schema(
    lint_disallowed_schema: core.Linter,
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test fail fix function disallowed schema."""
    sql_fail: str = """
    CREATE FUNCTION test.dup(int) RETURNS TABLE(f1 int) LANGUAGE SQL
    AS $$ SELECT $1 $$
    ;
    """

    sql_fix: str = "CREATE FUNCTION app.dup(integer)\nRETURNS TABLE (f1 integer)\nLANGUAGE sql\nAS $$ SELECT $1 $$;"  # noqa: E501

    disallowed_schema.config.lint.fix = True

    violations: core.ViolationMetric = lint_disallowed_schema.run(
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


def test_fail_enum_disallowed_schema(
    lint_disallowed_schema: core.Linter,
) -> None:
    """Test fail enum disallowed schema."""
    sql_fail: str = "CREATE TYPE test.mood AS ENUM ('sad', 'ok');"

    violations: core.ViolationMetric = lint_disallowed_schema.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_fix_enum_disallowed_schema(
    lint_disallowed_schema: core.Linter,
    disallowed_schema: core.BaseChecker,
) -> None:
    """Test fail fix enum disallowed schema."""
    sql_fail: str = "CREATE TYPE test.mood AS ENUM ('sad', 'ok');"

    sql_fix: str = "CREATE TYPE app.mood AS ENUM (\n    'sad'\n  , 'ok'\n);"

    disallowed_schema.config.lint.fix = True

    violations: core.ViolationMetric = lint_disallowed_schema.run(
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
