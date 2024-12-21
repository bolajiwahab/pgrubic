"""Core functionalities."""

from pgrubic.core import cache, config
from pgrubic.core.cache import Cache
from pgrubic.core.config import Config, parse_config
from pgrubic.core.linter import Linter, BaseChecker, ViolationStats
from pgrubic.core.loader import (
    load_rules,
    load_formatters,
    add_apply_fix_to_rule,
    add_set_locations_to_rule,
)
from pgrubic.core.logger import logger
from pgrubic.core.filters import filter_sources
from pgrubic.core.formatter import Formatter

__all__ = [
    "BaseChecker",
    "Cache",
    "Config",
    "Formatter",
    "Linter",
    "ViolationStats",
    "add_apply_fix_to_rule",
    "add_set_locations_to_rule",
    "cache",
    "config",
    "filter_sources",
    "load_formatters",
    "load_rules",
    "logger",
    "parse_config",
]
