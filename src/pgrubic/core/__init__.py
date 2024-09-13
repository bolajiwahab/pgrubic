"""Core functionalities."""

from pgrubic.core.config import Config, parse_config
from pgrubic.core.linter import Linter, BaseChecker, ViolationMetric
from pgrubic.core.loader import (
    load_rules,
    add_apply_fix_to_rule,
    add_set_locations_to_rule,
)
from pgrubic.core.formatters import ddl, dml

__all__ = [
    "Linter",
    "BaseChecker",
    "ViolationMetric",
    "load_rules",
    "add_apply_fix_to_rule",
    "add_set_locations_to_rule",
    "parse_config",
    "Config",
    "ddl",
    "dml",
]
