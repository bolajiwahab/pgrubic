"""Test noqa."""

import typing

from colorama import Fore, Style

from tests import TEST_FILE
from pgrubic.core import noqa


def test_extract_star_ignore_from_inline_comments() -> None:
    """Test extract star ignore from inline comments."""
    source_code: str = """
    -- noqa
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    assert inline_ignores[0].rule == noqa.A_STAR


def test_extract_ignores() -> None:
    """Test extract ignores from inline comments."""
    source_code: str = """-- pgrubic: noqa: NM016, GN001
    -- noqa: NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
        source_file=str(TEST_FILE),
        source_code=source_code,
    )

    assert inline_ignores[0].rule == "NM016"
    assert inline_ignores[1].rule == "GN001"


def test_extract_ignores_length() -> None:
    """Test extract ignore from inline comments length."""
    source_code: str = """
    -- noqa: NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    expected_ignores_length: int = 2

    assert len(inline_ignores) == expected_ignores_length


def test_wrongly_formed_inline_ignores_from_inline_comments(capfd: typing.Any) -> None:
    """Test extract ignore from inline comments."""
    source_code: str = """
    -- noqa NM016, GN001
    CREATE TABLE tbl (activated date);
    """

    noqa.extract_ignores(source_file=TEST_FILE, source_code=source_code)

    _, err = capfd.readouterr()

    assert (
        err
        == f"{Fore.YELLOW}Warning: Malformed `noqa` directive at location 5. Expected `noqa: <rules>`{Style.RESET_ALL}\n"  # noqa: E501
    )


def test_report_specific_unused_ignores(
    capfd: typing.Any,
) -> None:
    """Test report specific unused ignores."""
    source_code: str = """
    -- noqa: NM016
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    noqa.report_unused_ignores(source_file=TEST_FILE, inline_ignores=inline_ignores)
    out, _ = capfd.readouterr()
    assert (
        out
        == f"{TEST_FILE}:3:52: {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL} (unused: {Fore.RED}{Style.BRIGHT}NM016{Style.RESET_ALL})\n"  # noqa: E501
    )


def test_report_general_unused_ignores(
    capfd: typing.Any,
) -> None:
    """Test report general unused ignores."""
    source_code: str = """
    -- noqa
    CREATE TABLE tbl (activated date);
    """

    inline_ignores: list[noqa.NoQaDirective] = noqa.extract_ignores(
        source_file=TEST_FILE,
        source_code=source_code,
    )

    noqa.report_unused_ignores(source_file=TEST_FILE, inline_ignores=inline_ignores)
    out, _ = capfd.readouterr()
    assert (
        out
        == f"{TEST_FILE}:3:45: {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL} (unused: {Fore.RED}{Style.BRIGHT}{noqa.A_STAR}{Style.RESET_ALL})\n"  # noqa: E501
    )
