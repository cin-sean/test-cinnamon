from enum import Enum

class OperationType(str, Enum):
    MUTABLE = "mutable"
    IMMUTABLE = "immutable"
    CHORD = "chord"
    SHORTHAND_CHAINING = "shorthand-chaining"
    CHORD_WITH_CALLBACK = "chord-with-callback"
