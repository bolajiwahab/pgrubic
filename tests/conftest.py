"""Conftest."""

import enum
import typing
import pathlib
import contextlib

import yaml
import pytest

from pgrubic import core


@pytest.fixture(scope="module")
def linter() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    rules: set[type[core.BaseChecker]] = core.load_rules(
        config=config,
        include_deprecated=True,
    )

    linter = core.Linter(config=config, formatters=core.load_formatters)

    for rule in rules:
        linter.checkers.add(rule(config=config))

    return linter


@pytest.fixture(scope="session")
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


def _update_config(*, config: typing.Any, overrides: dict[str, typing.Any]) -> None:
    """Update a config object with overrides."""
    for key, value in overrides.items():
        if isinstance(value, dict):
            # If value is a dictionary, recursively update the nested config attribute
            _update_config(config=getattr(config, key), overrides=value)
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


def _restore_config(*, config: typing.Any, previous_config: typing.Any) -> None:
    """Restore a config snapshot while preserving the root object."""
    for field_name in type(config).model_fields:
        setattr(config, field_name, getattr(previous_config, field_name))


@contextlib.contextmanager
def update_config(
    *,
    config: core.Config,
    overrides: dict[str, typing.Any],
) -> typing.Iterator[None]:
    """Temporarily update a config object with overrides."""
    previous_config = config.model_copy(deep=True)
    try:
        _update_config(config=config, overrides=overrides)
        yield
    finally:
        _restore_config(config=config, previous_config=previous_config)
