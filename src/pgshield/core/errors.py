"""pgshield errors."""


class SQLBaseError(Exception):
    """Base class for all exceptions."""


class SQLParseError(SQLBaseError):
    """Parse error."""


class SQLLintError(SQLBaseError):
    """Lint error."""

class DuplicateRuleDetectedError(SQLBaseError):
    """Raised when duplicate rule is detected."""


class DuplicateConfigDetectedError(SQLBaseError):
    """Raised when duplicate config is detected."""


class ConfigMissingKeyError(SQLBaseError):
    """Raised when there is a config error."""
