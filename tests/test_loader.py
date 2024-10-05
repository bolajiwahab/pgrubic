"""Test loader."""

from pgrubic import core


def test_load_rules(linter: core.Linter) -> None:
    """Test loading rules."""
    expected_number_of_rules = 100

    rules = core.load_rules(config=linter.config)

    assert len(rules) == expected_number_of_rules
