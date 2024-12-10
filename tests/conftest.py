"""Conftest."""

import enum
import typing
import pathlib

import yaml
import pytest

from pgrubic import core


@pytest.fixture(scope="module")
def linter() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    core.BaseChecker.config = config

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    linter = core.Linter(config=config, formatters=core.load_formatters)

    for rule in rules:
        linter.checkers.add(rule())

    return linter


@pytest.fixture(scope="module")
def formatter() -> core.Formatter:
    """Setup formatters."""
    config: core.Config = core.parse_config()

    return core.Formatter(config=config, formatters=core.load_formatters)


@pytest.fixture
def cache(tmp_path: pathlib.Path) -> core.Cache:
    """Initialize cache."""
    config: core.Config = core.parse_config()
    config.cache_dir = tmp_path

    return core.Cache(config=config)


class TestCaseType(enum.StrEnum):
    """Test case type."""

    RULE = enum.auto()
    FORMATTER = enum.auto()


def load_test_cases(
    *,
    test_case_type: TestCaseType,
    directory: pathlib.Path,
) -> list[tuple[str, ...]]:
    """Load test cases from directory..

    Parameters
    ----------
    test_case_type: TestCaseType
        Type of test case.

    directory: pathlib.Path
        Directory to load test cases from.

    Returns:
    -------
    list[tuple[str, ...]]

    """
    test_cases: list[tuple[str, ...]] = []

    for file in sorted(directory.rglob("*.yml"), key=lambda x: x.name):
        with file.open() as f:
            content: dict[str, typing.Any] = yaml.safe_load(f)

        parent = content.pop(test_case_type)
        test_cases.extend((parent, (parent + "_" + k), v) for k, v in content.items())
    return test_cases


def update_config(config: core.Config, overrides: dict[str, typing.Any]) -> None:
    """Update config object with overrides."""
    for key, value in overrides.items():
        if isinstance(value, dict):
            # If value is a dictionary, recursively update the nested config attribute
            sub_config = getattr(config, key)
            update_config(sub_config, value)
        elif key == "required_columns":
            # Ensure required_columns is a list of columns
            setattr(
                config,
                key,
                [
                    core.config.Column(name=col["name"], data_type=col["data_type"])
                    for col in value
                ],
            )
        elif key == "disallowed_schemas":
            # Ensure disallowed_schemas is a list of disallowed_schema
            setattr(
                config,
                key,
                [
                    core.config.DisallowedSchema(
                        name=col["name"],
                        reason=col["reason"],
                        use_instead=col["use_instead"],
                    )
                    for col in value
                ],
            )
        elif key == "disallowed_data_types":
            # Ensure disallowed_types is a list of disallowed_type
            setattr(
                config,
                key,
                [
                    core.config.DisallowedDataType(
                        name=col["name"],
                        reason=col["reason"],
                        use_instead=col["use_instead"],
                    )
                    for col in value
                ],
            )
        else:
            # Set the attribute directly, e.g., config.format.lines_between_statements = 1
            setattr(config, key, value)
