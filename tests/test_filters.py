"""Test filters."""

import os
import pathlib
from unittest.mock import patch

import git
import pytest

from pgrubic import core
from pgrubic.core import noqa, config


def test_filter_linting_sources(tmp_path: pathlib.Path) -> None:
    """Test filter linting sources."""
    directory = tmp_path / "sub"
    directory.mkdir()

    sql_fail: str = "SELECT a = NULL;"

    sources: tuple[pathlib.Path, ...] = (
        pathlib.Path("test.sql"),
        pathlib.Path("test_main.sql"),
        pathlib.Path("test.py"),
        pathlib.Path("test.txt"),
        pathlib.Path("tables.sql"),
        pathlib.Path("views.sql"),
    )

    for source in sources:
        file_fail = directory / source
        file_fail.write_text(sql_fail)

    expected_sources_filtered_length = 2

    config_content = f"""
    include = [
        "*.py",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test_main.sql",
    ]
    [lint]
    include = [
        "*.sql",
        "*.txt",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test.sql",
    ]
    """

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory)},
    ):
        parsed_config = config.parse_config()

        sources_filtered = core.filter_sources(
            sources=(directory,),
            include=parsed_config.lint.include,
            exclude=parsed_config.lint.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length


def test_filter_formatting_sources(tmp_path: pathlib.Path) -> None:
    """Test filter formatting sources."""
    directory = tmp_path / "sub"
    directory.mkdir()

    sql_fail: str = "SELECT a = NULL;"

    sources: tuple[pathlib.Path, ...] = (
        pathlib.Path("test.sql"),
        pathlib.Path("test_main.sql"),
        pathlib.Path("test.py"),
        pathlib.Path("test.txt"),
        pathlib.Path("tables.sql"),
        pathlib.Path("views.sql"),
    )

    for source in sources:
        file_fail = directory / source
        file_fail.write_text(sql_fail)

    expected_sources_filtered_length = 2

    config_content = f"""
    include = [
        "*.py",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test_main.sql",
    ]
    [format]
    include = [
        "*.sql",
        "*.txt",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test.sql",
    ]
    """

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory)},
    ):
        parsed_config = config.parse_config()

        sources_filtered = core.filter_sources(
            sources=(directory,),
            include=parsed_config.format.include,
            exclude=parsed_config.format.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length


def test_respect_gitignore_filter_sources(tmp_path: pathlib.Path) -> None:
    """Test respect gitignore filter sources."""
    git.Repo.init(tmp_path)

    # Create a .gitignore file in the repository
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text(
        f"ignored_file.sql{noqa.NEW_LINE}café.sql{noqa.NEW_LINE}ignored_directory/{noqa.NEW_LINE}",
        encoding="utf-8",
    )

    directory = tmp_path / "sub"
    (directory / "ignored_directory").mkdir(parents=True)

    sql_fail: str = "SELECT a = NULL;"

    sources: tuple[pathlib.Path, ...] = (
        pathlib.Path("test.sql"),
        pathlib.Path("test_main.sql"),
        pathlib.Path("test.py"),
        pathlib.Path("test.txt"),
        pathlib.Path("ignored_file.sql"),
        pathlib.Path("café.sql"),
        pathlib.Path("ignored_directory/tables.sql"),
        pathlib.Path("tables.sql"),
        pathlib.Path("views.sql"),
    )

    for source in sources:
        file_fail = directory / source
        file_fail.write_text(sql_fail)

    expected_sources_filtered_length = 2

    config_content = f"""
    include = [
        "*.sql",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test_main.sql",
        "{str(directory).replace(os.path.sep, "/")}/test.sql",
    ]
    """

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {
            config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory),
            "GIT_CONFIG_GLOBAL": os.devnull,
        },
    ):
        parsed_config = config.parse_config()

        sources_filtered = core.filter_sources(
            sources=(directory,),
            include=parsed_config.include,
            exclude=parsed_config.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length


def test_respect_gitignore_false_filter_sources(tmp_path: pathlib.Path) -> None:
    """Test respect gitignore false filter sources."""
    git.Repo.init(tmp_path)

    # Create a .gitignore file in the repository
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text(f"ignored_file.sql{noqa.NEW_LINE}")

    directory = tmp_path / "sub"
    directory.mkdir()

    sql_fail: str = "SELECT a = NULL;"

    sources: tuple[pathlib.Path, ...] = (
        pathlib.Path("test.sql"),
        pathlib.Path("test_main.sql"),
        pathlib.Path("test.py"),
        pathlib.Path("test.txt"),
        pathlib.Path("ignored_file.sql"),
        pathlib.Path("tables.sql"),
        pathlib.Path("views.sql"),
    )

    for source in sources:
        file_fail = directory / source
        file_fail.write_text(sql_fail)

    expected_sources_filtered_length = 3

    config_content = f"""
    respect-gitignore = false
    include = [
        "*.sql",
    ]
    exclude = [
        "{str(directory).replace(os.path.sep, "/")}/test_main.sql",
        "{str(directory).replace(os.path.sep, "/")}/test.sql",
    ]
    """

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {
            config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory),
            "GIT_CONFIG_GLOBAL": os.devnull,
        },
    ):
        parsed_config = config.parse_config()

        sources_filtered = core.filter_sources(
            sources=(directory,),
            include=parsed_config.include,
            exclude=parsed_config.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length


def test_respect_gitignore_from_subdirectory(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test gitignore rules apply to relative sources when run from a subdirectory."""
    (tmp_path / ".gitignore").write_text(f"sub/ignored.sql{noqa.NEW_LINE}")
    directory = tmp_path / "sub"
    directory.mkdir()
    for name in ("ignored.sql", "kept.sql"):
        (directory / name).write_text("SELECT 1;")

    monkeypatch.chdir(directory)

    with patch.dict("os.environ", {"GIT_CONFIG_GLOBAL": os.devnull}):
        git.Repo.init(tmp_path)

        sources_filtered = core.filter_sources(
            sources=(pathlib.Path(),),
            include=[],
            exclude=[],
            respect_gitignore=True,
        )

        assert sources_filtered == {pathlib.Path("kept.sql")}


def test_respect_gitignore_keeps_named_sources(tmp_path: pathlib.Path) -> None:
    """Test sources named explicitly are kept, even when git ignores them."""
    (tmp_path / ".gitignore").write_text(f"ignored.sql{noqa.NEW_LINE}")
    source = tmp_path / "ignored.sql"
    source.write_text("SELECT 1;")

    with patch.dict("os.environ", {"GIT_CONFIG_GLOBAL": os.devnull}):
        git.Repo.init(tmp_path)

        sources_filtered = core.filter_sources(
            sources=(source,),
            include=[],
            exclude=[],
            respect_gitignore=True,
        )

        assert sources_filtered == {source}
