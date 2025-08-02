"""Tests for config."""

import pathlib
from unittest.mock import patch

import pytest

from pgrubic.core import config, errors


def test_config_from_environment_variable(tmp_path: pathlib.Path) -> None:
    """Test config from environment variable."""
    config_content = """
    [lint]
    fix = true
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory)},
    ):
        parsed_config = config.parse_config()
        assert parsed_config.lint.fix is True


def test_config_from_current_working_directory(tmp_path: pathlib.Path) -> None:
    """Test config from current working directory."""
    config_content = """
    [format]
    diff = true
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch("os.getcwd", return_value=str(directory)):
        assert pathlib.Path.cwd() == directory

        parsed_config = config.parse_config()
        assert parsed_config.format.diff is True


def test_missing_config_error(tmp_path: pathlib.Path) -> None:
    """Test missing config error."""
    config_content = """
    [lint]
    required-columns = [
        { name = "foo", type = "text" }
    ]
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch("os.getcwd", return_value=str(directory)):
        assert pathlib.Path.cwd() == directory

        with pytest.raises(errors.MissingConfigError) as excinfo:
            config.parse_config()

        assert excinfo.value.args[0] == "Missing config key: data-type"


def test_config_file_from_environment_variable_not_found_error() -> None:
    """Test config from environment variable not found error."""
    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: "directory"},
    ):
        with pytest.raises(errors.ConfigFileNotFoundError) as excinfo:
            config.parse_config()

        assert (
            excinfo.value.args[0]
            == """Config file "pgrubic.toml" not found in the path set in the environment variable PGRUBIC_CONFIG_PATH"""  # noqa: E501
        )


def test_config_parse_error(tmp_path: pathlib.Path) -> None:
    """Test config parse error."""
    config_content = """
    [lint]
    fix =
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory)},
    ):
        with pytest.raises(errors.ConfigParseError) as excinfo:
            config.parse_config()

        assert (
            excinfo.value.args[0]
            == f"""Error parsing configuration file "{config_file}\""""
        )
