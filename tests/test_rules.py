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
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    with conftest.update_config(config=linter.config, overrides=config_overrides):
        if parsed_test_case.sql_fail:
            # Set fix flag
            linter.config.lint.fix = bool(parsed_test_case.sql_fix)

            linting_result = linter.run(
                source_file=f"{parsed_test_case.rule}.sql",
                source_code=parsed_test_case.sql_fail,
            )

            assert len(linting_result.errors) == 0, (
                "Test failed: Errors found in test case"
            )

            assert any(
                violation.rule_code == rule for violation in linting_result.violations
            ), f"Test failed: No violations found for rule: `{rule}` in `{test_id}`"

            if parsed_test_case.sql_fix:
                assert linting_result.fixed_source_code == parsed_test_case.sql_fix

                # Check that the fixed source_code is valid
                try:
                    parser.parse_sql(linting_result.fixed_source_code)
                except parser.ParseError as error:
                    msg = f"Formatted code is not a valid syntax: {error!s}"
                    raise ValueError(msg) from error

        if parsed_test_case.sql_pass:
            linting_result = linter.run(
                source_file=f"{parsed_test_case.rule}.sql",
                source_code=parsed_test_case.sql_pass,
            )

            assert len(linting_result.errors) == 0, (
                "Test failed: Errors found in test case"
            )

            assert not any(
                violation.rule_code == rule for violation in linting_result.violations
            ), (
                f"""Test failed: Violations found for rule: `{rule}` in `{test_id}` which should pass"""  # noqa: E501
            )


def test_duplicate_index_state_not_shared_across_linter_instances() -> None:
    """Regression test for GN025's seen_indexes leaking across checker instances.

    Deliberately builds its own Linter instead of using the module-scoped `linter`
    fixture: that fixture creates checkers once and reuses them for every
    parametrized case in this module, so it can't distinguish state that's scoped
    to one checker instance from state that's shared at the class level (which is
    exactly the bug being guarded against here).
    """
    sql = "CREATE INDEX idx ON tbl (col);"

    for _ in range(2):
        config = core.parse_config()
        linter = core.Linter(config=config, formatters=core.load_formatters)
        for rule in core.load_rules(config=config, include_deprecated=True):
            linter.checkers.add(rule(config=config))

        linting_result = linter.run(source_file="test.sql", source_code=sql)

        assert not any(
            violation.rule_code == "GN025" for violation in linting_result.violations
        ), "Test failed: index flagged as duplicate across independent Linter instances"
