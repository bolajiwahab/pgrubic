"""Test formatter."""

import pytest

from tests import TEST_FILE
from pgrubic import core


def test_format(formatter: core.Formatter) -> None:
    """Test format."""
    source_code = "select 1;"
    expected_output: str = "SELECT 1;\n"
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code == expected_output


def test_skip_format(formatter: core.Formatter) -> None:
    """Test skip format."""
    source_code = "-- fmt: skip\nselect 1;\n"
    #     expected_output: str = """-- fmt: skip
    # select 1;\n;
    # """
    formatted_source_code = formatter.format(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert formatted_source_code == source_code


def test_format_parse_error(formatter: core.Formatter) -> None:
    """Test format."""
    source_code = "SELECT * FROM;"
    with pytest.raises(SystemExit) as excinfo:
        formatter.format(source_file=TEST_FILE, source_code=source_code)

    assert excinfo.value.code == 1
