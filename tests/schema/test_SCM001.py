"""Test for schemaunqualified objects."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.schema.SM001 import SchemaUnqualifiedObject


@pytest.fixture(scope="module")
def schema_unqualified_object() -> core.BaseChecker:
    """Create an instance of SchemaUnqualifiedObject."""
    return SchemaUnqualifiedObject()


@pytest.fixture
def lint_schema_unqualified_object(
    linter: core.Linter,
    schema_unqualified_object: core.BaseChecker,
) -> core.Linter:
    """Lint SchemaUnqualifiedObject."""
    linter.checkers.add(schema_unqualified_object)

    return linter


def test_schema_unqualified_object_rule_code(
    schema_unqualified_object: core.BaseChecker,
) -> None:
    """Test schema unqualified object rule code."""
    assert (
        schema_unqualified_object.code
        == schema_unqualified_object.__module__.split(".")[-1]
    )


def test_schema_unqualified_object_auto_fixable(
    schema_unqualified_object: core.BaseChecker,
) -> None:
    """Test schema unqualified object auto fixable."""
    assert schema_unqualified_object.is_auto_fixable is False


def test_pass_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail schema unqualified object."""
    sql_fail: str = "CREATE TABLE public.card();"

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_cte_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail schema unqualified object."""
    sql_fail: str = "WITH a AS (SELECT * FROM account) SELECT * FROM a;"

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail schema unqualified object."""
    sql_fail: str = "CREATE TABLE card();"

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_object_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail schema unqualified object."""
    sql_fail: str = "DROP TABLE mood;"

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_schema_unqualified_object_description(
    lint_schema_unqualified_object: core.Linter,
    schema_unqualified_object: core.BaseChecker,
) -> None:
    """Test fail schema unqualified object description."""
    sql_fail: str = "CREATE MATERIALIZED VIEW card AS SELECT * FROM account;"

    _: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(schema_unqualified_object.violations)).description
        == "Database object `card` should be schema qualified"
    )


def test_pass_noqa_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test pass noqa schema unqualified object."""
    sql_pass_noqa: str = "CREATE TABLE card AS SELECT * FROM account -- noqa: SM001;"

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail noqa schema unqualified object."""
    sql_noqa: str = """
    SELECT INTO card FROM public.account -- noqa: SM002
    ;
    """

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_schema_unqualified_object(
    lint_schema_unqualified_object: core.Linter,
) -> None:
    """Test fail noqa schema unqualified object."""
    sql_noqa: str = """
    CREATE TABLE card() -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_schema_unqualified_object.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
