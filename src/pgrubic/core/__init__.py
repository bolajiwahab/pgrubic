"""Core functionalities."""

from pgrubic.core import config
from pgrubic.core.config import Config, parse_config
from pgrubic.core.linter import Linter, BaseChecker, ViolationStats
from pgrubic.core.loader import (
    load_rules,
    load_formatters,
    add_apply_fix_to_rule,
    add_set_locations_to_rule,
)
from pgrubic.core.filters import filter_files
from pgrubic.core.logging import logger
from pgrubic.core.formatter import Formatter

__all__ = [
    "Linter",
    "Formatter",
    "BaseChecker",
    "ViolationStats",
    "load_rules",
    "load_formatters",
    "add_apply_fix_to_rule",
    "add_set_locations_to_rule",
    "config",
    "parse_config",
    "filter_files",
    "Config",
    "logger",
]
