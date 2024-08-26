"""pgrubic errors."""


class SQLBaseError(Exception):
    """Base class for all exceptions."""


class SQLParseError(Exception):
    """Raised when there is a SQL parse error."""


class ConfigMissingKeyError(SQLBaseError):
    """Raised when there is a config error."""
