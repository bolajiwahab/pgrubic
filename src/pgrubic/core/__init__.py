"""Core functionalities."""

from pgrubic.formatters import ddl, dml
from pgrubic.core.config import Config, parse_config
from pgrubic.core.linter import Linter, BaseChecker, ViolationMetric
from pgrubic.core.loader import (
    load_rules,
    add_apply_fix_to_rule,
    add_set_locations_to_rule,
)
from pgrubic.core.filters import filter_files
from pgrubic.core.formatter import Formatter, FormatResult

__all__ = [
    "Linter",
    "Formatter",
    "FormatResult",
    "BaseChecker",
    "ViolationMetric",
    "load_rules",
    "add_apply_fix_to_rule",
    "add_set_locations_to_rule",
    "parse_config",
    "filter_files",
    "Config",
    "ddl",
    "dml",
]
