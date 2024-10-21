"""Test formatter."""

import pytest

from tests import TEST_FILE
from pgrubic import core


def test_format_check(formatter: core.Formatter) -> None:
    """Test format check."""
    config: core.Config = core.parse_config()
    config.format.check = True
    source_code = "select 1;"
    expected_output: str = ""
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code.exit_code == 1
    assert formatted_source_code.output == expected_output


def test_format_diff(formatter: core.Formatter) -> None:
    """Test format diff."""
    config: core.Config = core.parse_config()
    config.format.check = False
    config.format.diff = True
    source_code = "select 1;"
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code.exit_code == 1
    assert len(formatted_source_code.output) > 0


def test_format(formatter: core.Formatter) -> None:
    """Test format."""
    config: core.Config = core.parse_config()
    config.format.check = False
    config.format.diff = False
    source_code = "select 1;"
    expected_output: str = "SELECT 1;\n"
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code.exit_code == 0
    assert formatted_source_code.output == expected_output


def test_format_parse_error(formatter: core.Formatter) -> None:
    """Test format."""
    source_code = "SELECT * FROM;"
    with pytest.raises(SystemExit) as excinfo:
        formatter.format(source_file=TEST_FILE, source_code=source_code)

    assert excinfo.value.code == 1
