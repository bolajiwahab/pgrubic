"""Test loader."""

from pgrubic import core


def test_load_rules(linter: core.Linter) -> None:
    """Test loading rules."""
    expected_active_rules = 113
    expected_total_rules = 114

    active_rules = core.load_rules(config=linter.config)
    all_rules = core.load_rules(config=linter.config, include_deprecated=True)

    assert "US011" not in {rule.code for rule in active_rules}
    assert "US011" in {rule.code for rule in all_rules}

    assert len(active_rules) == expected_active_rules
    assert len(all_rules) == expected_total_rules
