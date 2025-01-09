"""pgrubic errors."""


class BaseError(Exception):
    """Base class for all exceptions."""


class MissingConfigError(BaseError):
    """Raised when a config is missing."""


class ParseError(BaseError):
    """Raised when a parse error occurs."""


class MissingStatementTerminatorError(BaseError):
    """Raised when a statement terminator is missing."""
