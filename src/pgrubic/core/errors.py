"""pgrubic errors."""


class PgrubicError(Exception):
    """Base class for all exceptions."""


class MissingConfigError(PgrubicError):
    """Raised when a config is missing."""
