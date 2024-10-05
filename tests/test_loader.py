"""Test loader."""

from pgrubic.core import config, loader

_config = config.parse_config()


def test_load_rules() -> None:
    """Test loading rules."""
    expected_number_of_rules = 100

    rules = loader.load_rules(config=_config)

    assert len(rules) == expected_number_of_rules
