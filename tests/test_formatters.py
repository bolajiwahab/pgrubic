"""Test yaml test cases formatters."""

import typing
import pathlib

import pytest
from pglast import parser

from tests import TEST_FILE, conftest
from pgrubic import core
from pgrubic.core import noqa


@pytest.mark.parametrize(
    ("test_formatter", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.FORMATTER,
        directory=pathlib.Path("tests/fixtures/formatters"),
    ),
)
def test_formatters(
    formatter: core.Formatter,
    test_formatter: str,
    test_id: str,
    test_case: dict[str, str],
) -> None:
    """Test formatters."""
    config_overrides: dict[str, typing.Any] = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    # Apply overrides to global configuration
    conftest.update_config(formatter.config, config_overrides)

    result = formatter.format(
        source_file=TEST_FILE,
        source_code=test_case["sql"],
    )

    assert result.formatted_source_code == test_case["expected"], (
        f"Test failed for formatter: `{test_formatter}` in `{test_id}`"
    )

    # Check that the formatted source code is valid
    try:
        parser.parse_sql(result.formatted_source_code)
    except parser.ParseError as error:
        msg = f"Formatted code is not a valid syntax: {error!s}"
        raise ValueError(msg) from error


def test_format_parse_error(formatter: core.Formatter) -> None:
    """Test parse error."""
    source_code = "SELECT * FROM;"
    formatting_result = formatter.format(source_file=TEST_FILE, source_code=source_code)
    assert len(formatting_result.errors) == 1


def test_new_line_before_semicolon(formatter: core.Formatter) -> None:
    """Test new line before semicolon."""
    source_code = "select 1;"
    expected_output: str = f"SELECT 1{noqa.NEW_LINE};{noqa.NEW_LINE}"

    current_new_line_before_semicolon = formatter.config.format.new_line_before_semicolon

    formatter.config.format.new_line_before_semicolon = True

    result = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )
    formatter.config.format.new_line_before_semicolon = current_new_line_before_semicolon

    assert result.formatted_source_code == expected_output


def test_lowercase_keywords_preserves_other_tokens(formatter: core.Formatter) -> None:
    """Test lowercase keywords preserve other SQL token values."""
    source_code = """
SELECT Foo AS "FROM", 'WHERE' FROM Café -- JOIN
WHERE Foo::TEXT IS NOT NULL and name ILIKE '%postgres%';
"""

    expected_output = """-- JOIN
select foo as "FROM"
     , 'WHERE'
  from "café"
 where cast(foo as text) is not null
   and name ilike '%postgres%';
"""

    current_uppercase_keywords = formatter.config.format.uppercase_keywords

    formatter.config.format.uppercase_keywords = False

    result = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    formatter.config.format.uppercase_keywords = current_uppercase_keywords

    assert result.formatted_source_code == expected_output
