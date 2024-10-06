"""Test noqa."""

import typing

import pytest
from colorama import Fore, Style

from tests import SOURCE_PATH
from pgrubic.core import noqa, errors


def test_extract_star_ignore_from_inline_comments() -> None:
    """Test extract star ignore from inline comments."""
    source_code: str = """
    -- noqa:
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = (
        noqa.extract_ignores_from_inline_comments(source_code)
    )

    assert inline_ignores[0].rule == noqa.A_STAR


def test_extract_ignores_from_inline_comments() -> None:
    """Test extract ignores from inline comments."""
    source_code: str = """
    -- noqa: NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = (
        noqa.extract_ignores_from_inline_comments(source_code)
    )

    assert inline_ignores[0].rule == "NM016"
    assert inline_ignores[1].rule == "GN001"


def test_extract_ignores_from_inline_comments_length() -> None:
    """Test extract ignore from inline comments length."""
    source_code: str = """
    -- noqa: NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = (
        noqa.extract_ignores_from_inline_comments(source_code)
    )

    expected_ignores_length: int = 2

    assert len(inline_ignores) == expected_ignores_length


def test_wrongly_formed_inline_ignores_from_inline_comments() -> None:
    """Test extract ignore from inline comments."""
    source_code: str = """
    -- noqa NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    with pytest.raises(errors.SQLParseError) as excinfo:
        noqa.extract_ignores_from_inline_comments(source_code)

    assert (
        str(excinfo.value)
        == "Malformed 'noqa' section in line 5. Expected 'noqa: <rule>'"
    )


def test_report_unused_ignores(
    capfd: typing.Any,
) -> None:
    """Test report unused ignores."""
    source_code: str = """
    -- noqa: NM016
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = (
        noqa.extract_ignores_from_inline_comments(source_code)
    )

    noqa.report_unused_ignores(source_path=SOURCE_PATH, inline_ignores=inline_ignores)
    out, err = capfd.readouterr()
    assert (
        out
        == f"{SOURCE_PATH}:3:52: {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL} (unused: {Fore.RED}{Style.BRIGHT}NM016{Style.RESET_ALL})\n"  # noqa: E501
    )
