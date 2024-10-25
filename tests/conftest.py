"""Conftest."""

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
