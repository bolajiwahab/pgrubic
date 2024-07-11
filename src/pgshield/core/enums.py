"""Enums."""
import enum


class IdentityConstraintMode(enum.StrEnum):
    """Identity constraint mode."""

    IDENTITY_ALWAYS = "a"
    IDENTITY_BY_DEFAULT = "d"
