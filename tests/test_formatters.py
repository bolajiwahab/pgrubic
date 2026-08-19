"""Test yaml test cases formatters."""

import typing
import pathlib

import pytest
from pglast import parser, stream as pglast_stream

from tests import TEST_FILE, conftest
from pgrubic import core
from pgrubic.core import noqa, formatter as formatter_module


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

    with conftest.update_config(config=formatter.config, overrides=config_overrides):
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


def test_configured_streams(formatter: core.Formatter) -> None:
    """Test configured streams extend their corresponding pglast streams."""
    raw_stream = formatter_module.RawStream(config=formatter.config)
    indented_stream = formatter_module.IndentedStream(config=formatter.config)

    assert isinstance(raw_stream, pglast_stream.RawStream)
    assert raw_stream.config is formatter.config
    assert isinstance(indented_stream, pglast_stream.IndentedStream)
    assert indented_stream.config is formatter.config


def test_concatenate_nodes_with_type_cast(formatter: core.Formatter) -> None:
    """Test raw node concatenation uses the configured type-casting style."""
    with conftest.update_config(
        config=formatter.config,
        overrides={"format": {"type_casting_style": core.enums.TypeCastingStyle.NATIVE}},
    ):
        result = formatter.format(
            source_file=TEST_FILE,
            source_code="CREATE INDEX idx ON tbl ((CAST(value AS text)));",
        )

    assert result.formatted_source_code == (
        "CREATE INDEX idx\n    ON tbl ((value::text));\n"
    )


def test_format_parse_error(formatter: core.Formatter) -> None:
    """Test parse error."""
    source_code = "SELECT * FROM;"
    formatting_result = formatter.format(source_file=TEST_FILE, source_code=source_code)
    assert len(formatting_result.errors) == 1


def test_new_line_before_semicolon(formatter: core.Formatter) -> None:
    """Test new line before semicolon."""
    source_code = "select 1;"
    expected_output: str = f"SELECT 1{noqa.NEW_LINE};{noqa.NEW_LINE}"

    with conftest.update_config(
        config=formatter.config,
        overrides={"format": {"new_line_before_semicolon": True}},
    ):
        result = formatter.format(
            source_file=TEST_FILE,
            source_code=source_code,
        )

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

    with conftest.update_config(
        config=formatter.config,
        overrides={"format": {"uppercase_keywords": False}},
    ):
        result = formatter.format(
            source_file=TEST_FILE,
            source_code=source_code,
        )

    assert result.formatted_source_code == expected_output
