"""Test procedural language whitelist."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.security.ST002 import ProceduralLanguageWhitelist


@pytest.fixture(scope="module")
def procedural_language_whitelist() -> core.BaseChecker:
    """Create an instance of procedural language whitelist."""
    core.add_set_locations_to_rule(ProceduralLanguageWhitelist)
    return ProceduralLanguageWhitelist()


@pytest.fixture
def lint_procedural_language_whitelist(
    linter: core.Linter,
    procedural_language_whitelist: core.BaseChecker,
) -> core.Linter:
    """Lint procedural language whitelist."""
    procedural_language_whitelist.config.lint.allowed_languages = [
        "plpgsql",
    ]
    linter.checkers.add(procedural_language_whitelist)

    return linter


def test_procedural_language_whitelist_rule_code(
    procedural_language_whitelist: core.BaseChecker,
) -> None:
    """Test procedural language whitelist rule code."""
    assert (
        procedural_language_whitelist.code
        == procedural_language_whitelist.__module__.split(".")[-1]
    )


def test_procedural_language_whitelist_auto_fixable(
    procedural_language_whitelist: core.BaseChecker,
) -> None:
    """Test procedural language whitelist auto fixable."""
    assert procedural_language_whitelist.is_auto_fixable is False


def test_pass_allowed_language(
    lint_procedural_language_whitelist: core.Linter,
) -> None:
    """Test pass allowed language."""
    sql_fail: str = "CREATE LANGUAGE plpgsql;"

    violations: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_procedural_language_whitelist(
    lint_procedural_language_whitelist: core.Linter,
) -> None:
    """Test fail procedural language whitelist."""
    sql_fail: str = "CREATE LANGUAGE plsample HANDLER plsample_call_handler;"

    violations: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_procedural_language_whitelist_description(
    lint_procedural_language_whitelist: core.Linter,
    procedural_language_whitelist: core.BaseChecker,
) -> None:
    """Test procedural language whitelist description."""
    sql_fail: str = "CREATE LANGUAGE plsample HANDLER plsample_call_handler;"

    _: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(procedural_language_whitelist.violations),
        ).description
        == "Language 'plsample' is not allowed"
    )


def test_pass_noqa_procedural_language_whitelist(
    lint_procedural_language_whitelist: core.Linter,
) -> None:
    """Test pass noqa procedural language whitelist."""
    sql_pass_noqa: str = """
    -- noqa: ST002
    CREATE LANGUAGE plsample HANDLER plsample_call_handler;
    """

    violations: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_procedural_language_whitelist(
    lint_procedural_language_whitelist: core.Linter,
) -> None:
    """Test fail noqa procedural language whitelist."""
    sql_fail_noqa: str = """
    -- noqa: ST001
    CREATE LANGUAGE plsample HANDLER plsample_call_handler;
    """

    violations: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_procedural_language_whitelist(
    lint_procedural_language_whitelist: core.Linter,
) -> None:
    """Test pass noqa procedural language whitelist."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE LANGUAGE plsample HANDLER plsample_call_handler;
    """

    violations: core.ViolationMetric = lint_procedural_language_whitelist.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
