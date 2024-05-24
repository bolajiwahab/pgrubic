"""pgshield errors."""


class SQLBaseError(Exception):
    """Base class for all exceptions."""


class SQLParseError(SQLBaseError):
    """Parse error."""


class SQLLintError(SQLBaseError):
    """Lint error."""


class IndexNotConcurrentError(SQLBaseError):
    """Raised when index is not being built in a concurrent manner."""


class ForeignKeyConstraintShouldNotValidateExistingRowsError(SQLBaseError):
    """Raised when foreign key constraint is validating existing rows."""


class CheckConstraintShouldNotValidateExistingRowsError(SQLBaseError):
    """Raised when check constraint is validating existing rows."""


class UniqueConstraintShouldNotCreateUniqueIndexError(SQLBaseError):
    """Raised when unique constraint is creating a unique index."""


class NotNullConstraintOnExistingColumnError(SQLBaseError):
    """Raised when not null constraint is added to an existing column."""
