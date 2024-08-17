"""Conftest."""

import pytest

from pgshield import core


@pytest.fixture()
def linter() -> core.Linter:
    """Setup linter."""
    config: core.Config = core.parse_config()

    core.Checker.config = config

    return core.Linter(config=config)
