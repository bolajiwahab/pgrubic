"""Tests for config."""

import pathlib
from unittest.mock import patch

import pytest

from tests import conftest
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
    expected_compact_parenthesized_lists_margin = 100
    config_content = """
    [format]
    diff = true
    compact-parenthesized-lists-margin = 100
    uppercase-keywords = false
    rewrite-function-calls-as-equivalent-syntax = false
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch("os.getcwd", return_value=str(directory)):
        assert pathlib.Path.cwd() == directory

        parsed_config = config.parse_config()
        assert parsed_config.format.diff is True
        assert parsed_config.format.uppercase_keywords is False
        assert parsed_config.format.rewrite_function_calls_as_equivalent_syntax is False
        assert (
            parsed_config.format.compact_parenthesized_lists_margin
            == expected_compact_parenthesized_lists_margin
        )


def test_update_config_restores_previous_values() -> None:
    """Test temporary config overrides are restored on context exit."""
    parsed_config = config.parse_config()
    previous_margin = parsed_config.format.compact_parenthesized_lists_margin
    previous_fix = parsed_config.lint.fix

    new_compact_parenthesized_lists_margin = 20

    with conftest.update_config(
        config=parsed_config,
        overrides={
            "format": {
                "compact_parenthesized_lists_margin": new_compact_parenthesized_lists_margin,  # noqa: E501
            },
            "lint": {"fix": not previous_fix},
        },
    ):
        assert (
            parsed_config.format.compact_parenthesized_lists_margin
            == new_compact_parenthesized_lists_margin
        )
        assert parsed_config.lint.fix == (not previous_fix)

    assert parsed_config.format.compact_parenthesized_lists_margin == previous_margin
    assert parsed_config.lint.fix is previous_fix


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


def test_invalid_type_casting_style_error(tmp_path: pathlib.Path) -> None:
    """Test invalid type casting style error."""
    config_content = """
    [format]
    type-casting-style = "invalid"
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch("os.getcwd", return_value=str(directory)):
        assert pathlib.Path.cwd() == directory

        with pytest.raises(errors.InvalidConfigValueError) as excinfo:
            config.parse_config()

        assert (
            excinfo.value.args[0]
            == 'Invalid config value for key "format.type-casting-style": '
            '"invalid". Expected one of: "native", "standard", "literal"'
        )


def test_invalid_type_casting_style_error_suggests_close_match(
    tmp_path: pathlib.Path,
) -> None:
    """Test invalid type casting style error suggests a close match."""
    config_content = """
    [format]
    type-casting-style = "stand"
    """
    directory = tmp_path / "sub"
    directory.mkdir()
    (directory / config.CONFIG_FILE).write_text(config_content)

    with (
        patch("os.getcwd", return_value=str(directory)),
        pytest.raises(errors.InvalidConfigValueError) as excinfo,
    ):
        config.parse_config()

    assert (
        excinfo.value.args[0]
        == 'Invalid config value for key "format.type-casting-style": "stand". '
        'Did you mean "standard"? Expected one of: "native", "standard", "literal"'
    )


def test_invalid_non_string_type_casting_style_error(tmp_path: pathlib.Path) -> None:
    """Test invalid non-string type casting style error."""
    config_content = """
    [format]
    type-casting-style = 1
    """
    directory = tmp_path / "sub"
    directory.mkdir()
    (directory / config.CONFIG_FILE).write_text(config_content)

    with (
        patch("os.getcwd", return_value=str(directory)),
        pytest.raises(errors.InvalidConfigValueError) as excinfo,
    ):
        config.parse_config()

    assert (
        excinfo.value.args[0]
        == 'Invalid config value for key "format.type-casting-style": "1". '
        'Expected one of: "native", "standard", "literal"'
    )


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


def test_config_user_overrides(tmp_path: pathlib.Path) -> None:
    """Test config user overrides."""
    config_content = """
    [lint]
    fix = false
    """
    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(directory)},
    ):
        parsed_config = config.parse_config(overrides={"lint": {"fix": True}})
        assert parsed_config.lint.fix is True
