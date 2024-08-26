"""Conftest."""

import pytest

from pgrubic import core


@pytest.fixture
def linter() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    core.BaseChecker.config = config

    return core.Linter(config=config)
