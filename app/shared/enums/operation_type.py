from enum import StrEnum, auto

class OperationType(StrEnum):
    MUTABLE = auto()
    IMMUTABLE = auto()
    CHORD = auto()
    SHORTHAND_CHAINING = auto()
    CHORD_WITH_CALLBACK = auto()
