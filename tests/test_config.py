"""Tests for config."""

import typing
import pathlib
from unittest.mock import patch

import pytest
from pydantic import ValidationError

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

        assert excinfo.value.args[0] == (
            "Missing config key: lint.required-columns.0.data-type"
        )


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
            '"invalid". Expected one of: "native", "standard", "literal".'
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
        'Did you mean "standard"? Expected one of: "native", "standard", "literal".'
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
        'Expected one of: "native", "standard", "literal".'
    )


@pytest.mark.parametrize("section", ["lint", "format"])
def test_invalid_config_section(section: str) -> None:
    """Test configuration sections must be TOML tables."""
    with pytest.raises(errors.InvalidConfigValueError) as excinfo:
        config.parse_config(overrides={section: 1})

    assert excinfo.value.args[0] == (
        f'Invalid config value for key "{section}": "1". '
        "Expected a configuration section."
    )


@pytest.mark.parametrize(
    ("config_content", "expected_error"),
    [
        (
            '[lint]\nfix = "yes"\n',
            (
                'Invalid config value for key "lint.fix": "yes". '
                "Input should be a valid boolean."
            ),
        ),
        (
            '[format]\nlines-between-statements = "2"\n',
            (
                'Invalid config value for key "format.lines-between-statements": "2". '
                "Input should be a valid integer."
            ),
        ),
        (
            "[lint]\nignore = [1]\n",
            (
                'Invalid config value for key "lint.ignore.0": "1". '
                "Input should be a valid string."
            ),
        ),
        (
            "[format]\nunknown-config = true\n",
            (
                'Invalid config value for key "format.unknown-config": "True". '
                "Extra inputs are not permitted."
            ),
        ),
    ],
)
def test_invalid_user_config_value(
    tmp_path: pathlib.Path,
    config_content: str,
    expected_error: str,
) -> None:
    """Validate every value loaded from the user configuration."""
    (tmp_path / config.CONFIG_FILE).write_text(config_content)

    with (
        patch.dict(
            "os.environ",
            {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(tmp_path)},
        ),
        pytest.raises(errors.InvalidConfigValueError) as excinfo,
    ):
        config.parse_config()

    assert excinfo.value.args[0] == expected_error


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


def test_parsed_config_can_be_used_as_overrides() -> None:
    """Accept already validated configuration values as overrides."""
    parsed_config = config.parse_config()

    reparsed_config = config.parse_config(
        overrides=parsed_config.model_dump(by_alias=True),
    )

    assert reparsed_config == parsed_config


def test_parsed_config_reused_as_overrides_does_not_duplicate_include() -> None:
    """Reparsing a model_dump() must not duplicate lint/format include-exclude."""
    parsed_config = config.parse_config(
        overrides={"include": ["V*.sql"], "exclude": ["test*.sql"]},
    )

    reparsed_config = config.parse_config(
        overrides=parsed_config.model_dump(by_alias=True),
    )

    assert reparsed_config.lint.include == ["V*.sql"]
    assert reparsed_config.lint.exclude == ["test*.sql"]
    assert reparsed_config.format.include == ["V*.sql"]
    assert reparsed_config.format.exclude == ["test*.sql"]


def test_user_config_list_replaces_default(tmp_path: pathlib.Path) -> None:
    """Test user-configured lists replace default lists."""
    default_config = config.load_default_config()
    default_lint_config = typing.cast(dict[str, object], default_config["lint"])
    default_lint_config["ignore"] = ["TP001"]

    config_directory = tmp_path / "config"
    config_directory.mkdir()
    (config_directory / config.CONFIG_FILE).write_text(
        '[lint]\nignore = ["TP002"]\n',
    )

    with (
        patch.object(config, "load_default_config", return_value=default_config),
        patch.dict(
            "os.environ",
            {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(config_directory)},
        ),
    ):
        parsed_config = config.parse_config()

    assert parsed_config.lint.ignore == ["TP002"]


def test_override_list_replaces_user_config(tmp_path: pathlib.Path) -> None:
    """Test override lists replace user-configured lists."""
    (tmp_path / config.CONFIG_FILE).write_text(
        '[lint]\nignore = ["TP001"]\n',
    )

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: str(tmp_path)},
    ):
        parsed_config = config.parse_config(
            overrides={"lint": {"ignore": ["TP002"]}},
        )

    assert parsed_config.lint.ignore == ["TP002"]


@pytest.mark.parametrize(
    ("scope", "section", "included", "excluded"),
    [
        (config.ConfigScope.GENERAL, "lint", "select", "fix"),
        (config.ConfigScope.FILESYSTEM, "lint", "include", "fix"),
        (config.ConfigScope.INVOCATION, "lint", "fix", "include"),
        (config.ConfigScope.FILESYSTEM, "format", "include", "diff"),
        (config.ConfigScope.INVOCATION, "format", "diff", "include"),
    ],
)
def test_load_default_config_by_scope(
    scope: config.ConfigScope,
    section: str,
    included: str,
    excluded: str,
) -> None:
    """Load only defaults belonging to the requested scope."""
    defaults = config.load_default_config_by_scope(
        scope=scope,
    )
    section_defaults = defaults[section]

    assert isinstance(section_defaults, dict)
    assert included in section_defaults
    assert excluded not in section_defaults


def test_create_scoped_config_model_from_defaults_preserves_validation() -> None:
    """Keep source validators and reject fields outside the selected scope."""
    model = config.create_scoped_config_model_from_defaults(
        scope=config.ConfigScope.GENERAL,
    )

    with pytest.raises(ValidationError, match='Did you mean "standard"'):
        model.model_validate(
            {"lint": {}, "format": {"type-casting-style": "stand"}},
        )

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        model.model_validate({"lint": {"fix": True}, "format": {}})


def test_create_config_model_from_defaults_includes_every_scope() -> None:
    """Expose every packaged default through the complete config model."""
    model = config.create_config_model_from_defaults()
    dumped = model.model_validate({"lint": {}, "format": {}}).model_dump(
        by_alias=True,
        mode="json",
    )

    assert dumped == config.load_default_config()
