"""Conftest."""

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

    return core.Linter(config=config)


@pytest.fixture(scope="module")
def linter_new() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    core.BaseChecker.config = config

    rules: set[core.BaseChecker] = core.load_rules(config=config)

    linter = core.Linter(config=config)

    for rule in rules:
        linter.checkers.add(rule())

    return linter


@pytest.fixture(scope="module")
def formatter() -> core.Formatter:
    """Setup formatters."""
    config: core.Config = core.parse_config()

    return core.Formatter(config=config, formatters=core.load_formatters)


def load_test_cases(*, case: str, directory: pathlib.Path) -> list[tuple[str, ...]]:
    """Load test cases from directory..

    Parameters
    ----------
    case: str
        Case to load test for.

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

        prefix = content.pop(case)
        test_cases.extend((prefix + "_" + k, v) for k, v in content.items())
    return test_cases


def update_config(config: core.Config, overrides: dict[str, typing.Any]) -> None:
    """Update config object with overrides."""
    for key, value in overrides.items():
        if isinstance(value, dict):
            # If value is a dictionary, recursively update the nested config attribute
            sub_config = getattr(config, key)
            update_config(sub_config, value)
        else:
            # Set the attribute directly, e.g., config.format.lines_between_statements = 1
            setattr(config, key, value)
