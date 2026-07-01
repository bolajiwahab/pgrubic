"""Test loader."""

from pgrubic import core


def test_load_rules_deprecated_not_included(linter: core.Linter) -> None:
    """Test loading rules not including deprecated."""
    expected_number_of_rules = 114

    rules = core.load_rules(config=linter.config)

    assert len(rules) == expected_number_of_rules


def test_load_rules_deprecated_included(linter: core.Linter) -> None:
    """Test loading rules including deprecated."""
    expected_number_of_rules = 115

    rules = core.load_rules(config=linter.config, include_deprecated=True)

    assert len(rules) == expected_number_of_rules
