"""Test create rule."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN002 import CreateRule


@pytest.fixture(scope="module")
def create_rule() -> core.BaseChecker:
    """Create an instance of CreateRule."""
    core.add_set_locations_to_rule(CreateRule)
    return CreateRule()


@pytest.fixture
def lint_create_rule(
    linter: core.Linter,
    create_rule: core.BaseChecker,
) -> core.Linter:
    """Lint CreateRule."""
    linter.checkers.add(create_rule)

    return linter


def test_create_rule_rule_code(
    create_rule: core.BaseChecker,
) -> None:
    """Test create rule rule code."""
    assert create_rule.code == create_rule.__module__.split(".")[-1]


def test_create_rule_auto_fixable(
    create_rule: core.BaseChecker,
) -> None:
    """Test create rule auto fixable."""
    assert create_rule.is_auto_fixable is False


def test_fail_create_rule(
    lint_create_rule: core.Linter,
) -> None:
    """Test fail create rule."""
    sql_fail: str = "CREATE RULE notify_me AS ON UPDATE TO tbl DO ALSO NOTIFY tbl;"

    violations: core.ViolationMetric = lint_create_rule.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_create_rule_description(
    lint_create_rule: core.Linter,
    create_rule: core.BaseChecker,
) -> None:
    """Test create rule description."""
    sql_fail: str = "CREATE RULE notify_me AS ON UPDATE TO tbl DO ALSO NOTIFY tbl;"

    _: core.ViolationMetric = lint_create_rule.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(create_rule.violations),
        ).description
        == "Create rule detected"
    )


def test_pass_noqa_create_rule(
    lint_create_rule: core.Linter,
) -> None:
    """Test pass noqa create rule."""
    sql_pass_noqa: str = """
    -- noqa: GN002
    CREATE RULE notify_me AS ON UPDATE TO tbl DO ALSO NOTIFY tbl;
    """

    violations: core.ViolationMetric = lint_create_rule.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_create_rule(
    lint_create_rule: core.Linter,
) -> None:
    """Test fail noqa create rule."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE RULE notify_me AS ON UPDATE TO tbl DO ALSO NOTIFY tbl;
    """

    violations: core.ViolationMetric = lint_create_rule.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_create_rule(
    lint_create_rule: core.Linter,
) -> None:
    """Test fail noqa create rule."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE RULE notify_me AS ON UPDATE TO tbl DO ALSO NOTIFY tbl;
    """

    violations: core.ViolationMetric = lint_create_rule.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
