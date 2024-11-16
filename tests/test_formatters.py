"""Test yaml test cases formatters."""

import typing
import pathlib

import pytest

from tests import TEST_FILE
from pgrubic import core
from tests.conftest import update_config, load_test_cases


@pytest.mark.parametrize(
    ("test_id", "test_case"),
    load_test_cases(
        case="formatter",
        directory=pathlib.Path("tests/fixtures/formatters"),
    ),
)
def test_formatters(
    formatter: core.Formatter,
    test_id: str,
    test_case: dict[str, str],
) -> None:
    """Test formatters."""
    config_overrides: dict[str, typing.Any] = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    # Apply overrides to global configuration
    update_config(formatter.config, config_overrides)

    actual_output = formatter.format(
        source_file=TEST_FILE,
        source_code=test_case["sql"],
    )

    assert actual_output == test_case["expected"], f"Test failed: {test_id}"


def test_format_parse_error(formatter: core.Formatter) -> None:
    """Test format."""
    source_code = "SELECT * FROM;"
    with pytest.raises(SystemExit) as excinfo:
        formatter.format(source_file=TEST_FILE, source_code=source_code)

    assert excinfo.value.code == 1


def test_new_line_before_semicolon(formatter: core.Formatter) -> None:
    """Test new line before semicolon."""
    source_code = "select 1;"
    expected_output: str = "SELECT 1\n;\n"

    formatter.config.format.new_line_before_semicolon = True
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code == expected_output
