"""Test loader."""

from pgrubic.core import loader


def test_load_rules() -> None:
    """Test loading rules."""
    expected_number_of_rules = 100

    rules = loader.load_rules()

    assert len(rules) == expected_number_of_rules
