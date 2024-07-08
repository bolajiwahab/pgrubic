"""Enums."""
import enum


class KnownTypes:
    """Known types."""

    INTEGER = "integer"
    SMALLINT = "smallint"
    BIGINT = "bigint"
    REAL = "real"
    DOUBLE_PRECISION = "double precision"
    MONEY = "money"
    BOOLEAN = "boolean"
    DATE = "date"
    TIME = "time"
    TIMESTAMP = "timestamp"
    TIMESTAMPTZ = "timestamptz"


class IdentityConstraintMode(enum.StrEnum):
    """Identity constraint mode."""

    IDENTITY_ALWAYS = "a"
    IDENTITY_BY_DEFAULT = "d"
