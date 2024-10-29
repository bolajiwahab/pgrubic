"""Conftest."""

import typing

import pytest

from pgrubic import core


@pytest.fixture
def linter() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    core.BaseChecker.config = config

    return core.Linter(config=config)


@pytest.fixture
def formatter() -> core.Formatter:
    """Setup formatters."""
    config: core.Config = core.parse_config()

    return core.Formatter(config=config, formatters=core.load_formatters)


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
