"""Tests for config."""

import pathlib
from unittest.mock import patch

from pgrubic.core import config


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
