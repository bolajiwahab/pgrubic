"""Test filters."""

import os
import pathlib
from unittest.mock import patch

import git

from pgrubic import core
from pgrubic.core import config


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
        "{directory}/test_main.sql",
    ]
    [lint]
    include = [
        "*.sql",
        "*.txt",
    ]
    exclude = [
        "{directory}/test.sql",
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
        "{directory}/test_main.sql",
    ]
    [format]
    include = [
        "*.sql",
        "*.txt",
    ]
    exclude = [
        "{directory}/test.sql",
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
    # Disable global git config
    os.environ["GIT_CONFIG_GLOBAL"] = "/dev/null"

    git.Repo.init(tmp_path)

    # Create a .gitignore file in the repository
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("ignored_file.sql\n")

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

    expected_sources_filtered_length = 2

    config_content = f"""
    include = [
        "*.sql",
    ]
    exclude = [
        "{directory}/test_main.sql",
        "{directory}/test.sql",
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
            include=parsed_config.include,
            exclude=parsed_config.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length


def test_respect_gitignore_false_filter_sources(tmp_path: pathlib.Path) -> None:
    """Test respect gitignore false filter sources."""
    # Disable global git config
    os.environ["GIT_CONFIG_GLOBAL"] = "/dev/null"

    git.Repo.init(tmp_path)

    # Create a .gitignore file in the repository
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("ignored_file.sql\n")

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
        "{directory}/test_main.sql",
        "{directory}/test.sql",
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
            include=parsed_config.include,
            exclude=parsed_config.exclude,
            respect_gitignore=parsed_config.respect_gitignore,
        )

        assert len(sources_filtered) == expected_sources_filtered_length
