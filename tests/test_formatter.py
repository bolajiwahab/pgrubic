"""Test formatter entry point and streams."""

import typing
import pathlib

import pytest
from pglast import parser, stream as pglast_stream

from tests import TEST_FILE, conftest
from pgrubic import core
from pgrubic.core import formatter as formatter_module


@pytest.mark.parametrize(
    ("test_formatter", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.CORE,
        path=pathlib.Path("tests/fixtures/core/formatter.yml"),
    ),
)
def test_formatter(
    formatter: core.Formatter,
    test_formatter: str,
    test_id: str,
    test_case: dict[str, typing.Any],
) -> None:
    """Test the formatter entry point."""
    config_overrides = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    with conftest.update_config(config=formatter.config, overrides=config_overrides):
        result = formatter.format(
            source_file=TEST_FILE,
            source_code=test_case["sql"],
        )

    assert {error.message for error in result.errors} == set(
        test_case.get("expected_errors", []),
    ), f"Unexpected formatter errors: `{test_formatter}` in `{test_id}`"

    assert result.formatted_source_code == test_case["expected"], (
        f"Unexpected formatted source: `{test_formatter}` in `{test_id}`"
    )


def test_configured_streams(formatter: core.Formatter) -> None:
    """Test configured streams extend their corresponding pglast streams."""
    raw_stream = formatter_module.RawStream(config=formatter.config)
    indented_stream = formatter_module.IndentedStream(config=formatter.config)

    assert isinstance(raw_stream, pglast_stream.RawStream)
    assert raw_stream.config is formatter.config
    assert isinstance(indented_stream, pglast_stream.IndentedStream)
    assert indented_stream.config is formatter.config


def test_configured_streams_write_as_keyword(formatter: core.Formatter) -> None:
    """Test contextual SQL syntax follows configured keyword casing."""
    for stream_type in (formatter_module.RawStream, formatter_module.IndentedStream):
        output = stream_type(config=formatter.config)
        output.write_as_keyword("LOCALE_PROVIDER")
        assert output.getvalue() == "LOCALE_PROVIDER"

        with conftest.update_config(
            config=formatter.config,
            overrides={"format": {"uppercase_keywords": False}},
        ):
            output = stream_type(config=formatter.config)
            output.write_as_keyword("LOCALE_PROVIDER")
            assert output.getvalue() == "locale_provider"


def test_create_raw_stream_factory(formatter: core.Formatter) -> None:
    """Test the formatter creates fresh, consistently configured raw streams."""
    first_stream = formatter.create_raw_stream()
    second_stream = formatter.create_raw_stream()

    assert first_stream is not second_stream
    assert first_stream.config is formatter.config
    assert (
        first_stream.special_functions
        is formatter.config.format.rewrite_function_calls_as_equivalent_syntax
    )
    assert (
        first_stream.remove_pg_catalog_from_functions
        is formatter.config.format.remove_pg_catalog_from_functions
    )


def test_raw_stream_supports_custom_printers(formatter: core.Formatter) -> None:
    """Test custom printers support raw stream rendering."""
    assert formatter.create_raw_stream()("CREATE INDEX idx ON tbl (value)") == (
        "CREATE INDEX idx ON tbl (value)"
    )
    assert (
        formatter.create_raw_stream()(
            "CREATE TABLE tbl (value integer) WITH (fillfactor = 90)",
        )
        == "CREATE TABLE tbl (value integer) WITH (fillfactor = 90)"
    )


def test_check_constraint_rejects_raw_and_cooked_expressions(
    formatter: core.Formatter,
) -> None:
    """Test a CHECK constraint cannot contain both expression forms."""
    statement = parser.parse_sql("CREATE TABLE tbl (value integer CHECK (value > 0))")
    constraint = statement[0].stmt.tableElts[0].constraints[0]  # type: ignore[attr-defined]
    constraint.cooked_expr = "cooked expression"

    with pytest.raises(
        ValueError,
        match="CHECK constraint cannot have both raw and cooked expressions",
    ):
        formatter.create_raw_stream()(constraint)
