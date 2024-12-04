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
    "BaseChecker",
    "Config",
    "Formatter",
    "Linter",
    "ViolationStats",
    "add_apply_fix_to_rule",
    "add_set_locations_to_rule",
    "config",
    "filter_files",
    "load_formatters",
    "load_rules",
    "logger",
    "parse_config",
]
