"""Test noqa."""

import typing
import pathlib

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
        == f"{Fore.YELLOW}Warning: Malformed `noqa` directive at location 5. Expected `noqa: <rules>`{Style.RESET_ALL}{noqa.NEW_LINE}"  # noqa: E501
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
        == f"{TEST_FILE}:3:52: {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL} (unused: {Fore.RED}{Style.BRIGHT}NM016{Style.RESET_ALL}){noqa.NEW_LINE}"  # noqa: E501
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
        == f"{TEST_FILE}:3:45: {Fore.YELLOW}Unused noqa directive{Style.RESET_ALL} (unused: {Fore.RED}{Style.BRIGHT}{noqa.A_STAR}{Style.RESET_ALL}){noqa.NEW_LINE}"  # noqa: E501
    )


def test_add_file_level_general_ignore(tmp_path: pathlib.Path) -> None:
    """Test add file level general ignore."""
    directory = tmp_path / "sub"
    directory.mkdir()

    source_file1 = directory / "source_file1.sql"
    source_file1.write_text("SELECT * FROM tab")

    source_file2 = directory / "source_file2.sql"
    source_file2.write_text(f"-- pgrubic: noqa{noqa.NEW_LINE} SELECT * FROM tab")  # noqa: S608

    modified_sources = noqa.add_file_level_general_ignore(
        sources={source_file1, source_file2},
    )

    assert modified_sources == 1


def test_statement_without_semi_colon() -> None:
    """Test statements without semicolon."""
    source_code: str = """
    CREATE TABLE tbl (activated date)

    """

    extracted_statements = noqa.extract_statement_locations(source_code=source_code)

    assert extracted_statements[0].text == "CREATE TABLE tbl (activated date);"


def test_indented_statement_without_semi_colon() -> None:
    """Test statements without semicolon."""
    source_code: str = """
CREATE TABLE tbl (
    activated date
)

    """
    expected_statement = """CREATE TABLE tbl (
    activated date
);"""

    extracted_statements = noqa.extract_statement_locations(source_code=source_code)

    assert extracted_statements[0].text == expected_statement
