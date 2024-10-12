"""Test non concurrent index creation."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US016 import NonConcurrentIndexCreation


@pytest.fixture(scope="module")
def non_concurrent_index_creation() -> core.BaseChecker:
    """Create an instance of NonConcurrentIndexCreation."""
    core.add_apply_fix_to_rule(NonConcurrentIndexCreation)
    core.add_set_locations_to_rule(NonConcurrentIndexCreation)
    return NonConcurrentIndexCreation()


@pytest.fixture
def lint_non_concurrent_index_creation(
    linter: core.Linter,
    non_concurrent_index_creation: core.BaseChecker,
) -> core.Linter:
    """Lint NonConcurrentIndexCreation."""
    non_concurrent_index_creation.config.lint.fix = False
    linter.checkers.add(non_concurrent_index_creation)

    return linter


def test_non_concurrent_index_creation_rule_code(
    non_concurrent_index_creation: core.BaseChecker,
) -> None:
    """Test non concurrent index creation rule code."""
    assert (
        non_concurrent_index_creation.code
        == non_concurrent_index_creation.__module__.split(
            ".",
        )[-1]
    )


def test_non_concurrent_index_creation_auto_fixable(
    non_concurrent_index_creation: core.BaseChecker,
) -> None:
    """Test non concurrent index creation auto fixable."""
    assert non_concurrent_index_creation.is_auto_fixable is True


def test_pass_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
) -> None:
    """Test pass concurrent index creation."""
    sql_pass: str = "CREATE INDEX CONCURRENTLY idx ON public.card(account_id);"

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
) -> None:
    """Test non concurrent index creation."""
    sql_fail: str = "CREATE INDEX idx ON public.card(account_id);"

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_index_creation_description(
    lint_non_concurrent_index_creation: core.Linter,
    non_concurrent_index_creation: core.BaseChecker,
) -> None:
    """Test non concurrent index creation description."""
    sql_fail: str = "CREATE INDEX idx ON public.card(account_id);"

    _: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_concurrent_index_creation.violations),
        ).description
        == "Non concurrent index creation"
    )


def test_pass_noqa_non_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
) -> None:
    """Test pass noqa non concurrent index creation."""
    sql_pass_noqa: str = """
    -- noqa: US016
    CREATE INDEX idx ON public.card(account_id);
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
) -> None:
    """Test fail noqa non concurrent index creation."""
    sql_noqa: str = """
    -- noqa: US001
    CREATE INDEX idx ON public.card(account_id);
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_non_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
) -> None:
    """Test pass noqa non concurrent index creation."""
    sql_noqa: str = """
    -- noqa
    CREATE INDEX idx ON public.card(account_id);
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_non_concurrent_index_creation(
    lint_non_concurrent_index_creation: core.Linter,
    non_concurrent_index_creation: core.BaseChecker,
) -> None:
    """Test fail fix non concurrent index creation."""
    sql_fail: str = "CREATE INDEX idx ON public.card(account_id);"

    sql_fix: str = "CREATE INDEX CONCURRENTLY idx\n    ON public.card (account_id);"

    non_concurrent_index_creation.config.lint.fix = True

    violations: core.ViolationMetric = lint_non_concurrent_index_creation.run(
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
