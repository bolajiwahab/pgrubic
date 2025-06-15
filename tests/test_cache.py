"""Test cache."""

import os
import typing
import pathlib
from unittest.mock import patch

from pgrubic import core
from pgrubic.core import noqa

SOURCE_FILE: typing.Final[str] = "cache.sql"


def test_cache_file_existence(tmp_path: pathlib.Path, cache: core.Cache) -> None:
    """Test cache file existence."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    assert not cache.cache_file.exists()

    cache.write(sources={source})

    assert cache.cache_file.exists()


def test_source_not_in_cache(tmp_path: pathlib.Path, cache: core.Cache) -> None:
    """Test source not in cache."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source_1 = directory / "source_1.sql"
    source_1.write_text(source_code)

    source_2 = directory / "source_2.sql"
    source_2.write_text(source_code)

    source_3 = directory / "source_3.sql"
    source_3.write_text(source_code)

    sources_to_be_formatted = cache.filter_sources(
        sources={source_1, source_2},
    )

    assert len(sources_to_be_formatted) == 2  # noqa: PLR2004

    cache.write(sources={source_1, source_2})

    sources_to_be_formatted = cache.filter_sources(
        sources={source_1, source_2},
    )

    assert len(sources_to_be_formatted) == 0

    # Force recaching source_1, source_2 should still be in the cache
    cache.write(sources={source_1})

    sources_to_be_formatted = cache.filter_sources(
        sources={source_1, source_2},
    )

    assert len(sources_to_be_formatted) == 0

    # Add a new source
    sources_to_be_formatted = cache.filter_sources(
        sources={source_1, source_2, source_3},
    )

    assert len(sources_to_be_formatted) == 1

    cache.write(sources={source_3})

    sources_to_be_formatted = cache.filter_sources(
        sources={source_1, source_2, source_3},
    )

    assert len(sources_to_be_formatted) == 0


def test_source_in_cache(tmp_path: pathlib.Path, cache: core.Cache) -> None:
    """Test source in cache."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 1

    cache.write(sources={source})

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 0


def test_source_invalidated_in_cache_by_modified_time(
    tmp_path: pathlib.Path,
    cache: core.Cache,
) -> None:
    """Test source invalidated in cache by modified time."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    cache.write(sources={source})

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 0

    # Change the modified time of source
    os.utime(source, (1602179630, 1602179630))

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 1


def test_source_invalidated_in_cache_by_size(
    tmp_path: pathlib.Path,
    cache: core.Cache,
) -> None:
    """Test source invalidated in cache by size."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    cache.write(sources={source})

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 0

    # Add a new line to source
    source.write_text(source_code + noqa.NEW_LINE)

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 1


def test_source_invalidated_in_cache_by_content(
    tmp_path: pathlib.Path,
    cache: core.Cache,
) -> None:
    """Test source invalidated in cache by content."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    cache.write(sources={source})

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 0

    # Update a character in source
    source.write_text("SELECT b = NULL;")

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 1


def test_source_invalidated_in_cache_by_config(
    tmp_path: pathlib.Path,
    cache: core.Cache,
) -> None:
    """Test source invalidated in cache by config."""
    source_code: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    source = directory / SOURCE_FILE
    source.write_text(source_code)

    cache.write(sources={source})

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 0

    cache.config.format.new_line_before_semicolon = True

    sources_to_be_formatted = cache.filter_sources(
        sources={source},
    )

    assert len(sources_to_be_formatted) == 1


def test_cache_directory_from_environment_variable_default_in_config(
    tmp_path: pathlib.Path,
) -> None:
    """Test cache directory from environment variable default in config."""
    config = core.parse_config()
    config.cache_dir = pathlib.Path(core.cache.DEFAULT_CACHE_DIR)

    with patch.dict(
        "os.environ",
        {core.cache.CACHE_DIR_ENVIRONMENT_VARIABLE: str(tmp_path)},
    ):
        cache = core.Cache(config=config)
        assert cache.config.cache_dir == tmp_path


def test_cache_directory_from_environment_variable_non_default_in_config(
    tmp_path: pathlib.Path,
) -> None:
    """Test cache directory from environment variable non default in config."""
    config = core.parse_config()
    config.cache_dir = pathlib.Path()

    with patch.dict(
        "os.environ",
        {core.cache.CACHE_DIR_ENVIRONMENT_VARIABLE: str(tmp_path)},
    ):
        cache = core.Cache(config=config)
        assert cache.config.cache_dir != tmp_path
