"""Test loader."""

from pgrubic import core


def test_load_rules(linter: core.Linter) -> None:
    """Test loading rules."""
    expected_active_rules = 117
    expected_total_rules = 118

    active_rules = core.load_rules(config=linter.config)
    all_rules = core.load_rules(config=linter.config, include_deprecated=True)

    actual_active_rules = len(active_rules)
    actual_total_rules = len(all_rules)

    assert "US011" not in {rule.code for rule in active_rules}
    assert "US011" in {rule.code for rule in all_rules}

    assert actual_active_rules == expected_active_rules, (
        f"expected {expected_active_rules} active rules but got {actual_active_rules}"
    )
    assert actual_total_rules == expected_total_rules, (
        f"expected {expected_total_rules} rules but got {actual_total_rules}"
    )
