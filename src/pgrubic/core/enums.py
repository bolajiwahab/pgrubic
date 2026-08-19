"""Enums."""

import enum


class FunctionOption(enum.StrEnum):
    """Function option."""

    SECURITY = enum.auto()
    LANGUAGE = enum.auto()
    SET = enum.auto()


class TypeCastingStyle(enum.StrEnum):
    """Type-casting output style."""

    NATIVE = enum.auto()
    STANDARD = enum.auto()
    LITERAL = enum.auto()
