"""Test linter."""

import typing
import pathlib

import pytest

from tests import conftest
from pgrubic import DOCUMENTATION_URL, RULE_DOCUMENTATION_BASE, core

SOURCE_FILE = "linter.sql"


@pytest.mark.parametrize(
    ("fixture_group", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.CORE,
        path=pathlib.Path("tests/fixtures/core/linter.yml"),
    ),
)
def test_linter(
    linter: core.Linter,
    fixture_group: str,  # noqa: ARG001
    test_id: str,  # noqa: ARG001
    test_case: dict[str, typing.Any],
) -> None:
    """Test linter behavior."""
    config_overrides = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    with conftest.update_config(config=linter.config, overrides=config_overrides):
        result = linter.run(
            source_file=SOURCE_FILE,
            source_code=test_case["sql"],
        )

    expected_violations = set(test_case.get("violations", []))
    actual_violations = {violation.rule_code for violation in result.violations}
    if expected_violations:
        assert actual_violations == expected_violations, (
            f"Expected {expected_violations} violations, got {actual_violations}"
        )

    expected_errors = set(test_case.get("errors", []))
    actual_errors = {error.message for error in result.errors}
    if expected_errors:
        assert actual_errors == expected_errors, (
            f"Expected {expected_errors} errors, got {actual_errors}"
        )

    expected_fixes = test_case.get("fixes")
    actual_fixes = result.fixed_source_code
    if expected_fixes:
        assert expected_fixes == actual_fixes, (
            f"Expected {expected_fixes}, got {actual_fixes}"
        )


def test_linter_generate_lint_report(
    linter: core.Linter,
    tmp_path: pathlib.Path,
) -> None:
    """Test linter lint report."""
    directory = tmp_path / "sub"
    directory.mkdir()
    report_file = directory / "report.md"

    # The ordering of violations is not guaranteed
    # So we only check for one violation here
    lint_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="SELECT a = NULL; SELECT b FROM;",
    )

    linter.generate_lint_report(
        lint_results=[lint_result],
        report_file=str(report_file),
    )

    expected_lint_report = f"""## Pgrubic Lint Report

Total violations: **1**

Total errors: **1**

<details>
<summary>Violations (1)</summary>

| File | Line | Col | Rule | Description | Help |
|------|------|-----|------|-------------|------|
| linter.sql | 1 | 10 | [GN024]({DOCUMENTATION_URL}/{RULE_DOCUMENTATION_BASE}/general/null-comparison) | Comparison with NULL should be [IS | IS NOT] NULL | Use [IS | IS NOT] NULL |
</details>

<details>
<summary>Errors (1)</summary>

| File | Message | Hint |
|------|---------|------|
| linter.sql | syntax error at or near ";", at index 14 | Make sure the statement is valid PostgreSQL statement. If it is, please report this issue at https://github.com/bolajiwahab/pgrubic/issues |
</details>
"""  # noqa: E501

    assert report_file.read_text() == expected_lint_report
