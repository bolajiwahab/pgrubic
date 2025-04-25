"""Test yaml test cases rules."""

import typing
import pathlib

import pytest
from pglast import parser

from tests import conftest
from pgrubic import core


class RuleTestCase(typing.NamedTuple):
    """Rule test case."""

    rule: str
    sql_fail: str | None
    sql_pass: str | None
    sql_fix: str | None


@pytest.mark.parametrize(
    ("rule", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.RULE,
        directory=pathlib.Path("tests/fixtures/rules"),
    ),
)
def test_rules(
    linter: core.Linter,
    rule: str,
    test_id: str,
    test_case: dict[str, str],
) -> None:
    """Test rules."""
    parsed_test_case = RuleTestCase(
        rule=rule,
        sql_fail=test_case.get("sql_fail"),
        sql_pass=test_case.get("sql_pass"),
        sql_fix=test_case.get("sql_fix"),
    )

    config_overrides: dict[str, typing.Any] = typing.cast(
        "dict[str, typing.Any]",
        test_case.get("config", {}),
    )

    # Apply overrides to global configuration
    conftest.update_config(linter.config, config_overrides)

    if parsed_test_case.sql_fail:
        # Set fix flag
        linter.config.lint.fix = bool(parsed_test_case.sql_fix)

        linting_result = linter.run(
            source_file=f"{parsed_test_case.rule}.sql",
            source_code=parsed_test_case.sql_fail,
        )

        assert any(
            violation.rule_code == rule for violation in linting_result.violations
        ), f"Test failed: No violations found for rule: `{rule}` in `{test_id}`"

        if parsed_test_case.sql_fix:
            assert linting_result.fixed_sql == parsed_test_case.sql_fix

            # Check that the fixed sql is valid
            try:
                parser.parse_sql(linting_result.fixed_sql)
            except parser.ParseError as error:
                msg = f"Formatted code is not a valid syntax: {error!s}"
                raise ValueError(msg) from error

    if parsed_test_case.sql_pass:
        linting_result = linter.run(
            source_file=f"{parsed_test_case.rule}.sql",
            source_code=parsed_test_case.sql_pass,
        )

        assert not any(
            violation.rule_code == rule for violation in linting_result.violations
        ), (
            f"""Test failed: Violations found for rule: `{rule}` in `{test_id}` which should pass"""  # noqa: E501
        )
