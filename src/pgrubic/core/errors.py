"""pgrubic errors."""


class SQLBaseError(Exception):
    """Base class for all exceptions."""


class SQLParseError(SQLBaseError):
    """Raised when there is a SQL parse error."""
