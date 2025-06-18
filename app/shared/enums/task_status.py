from enum import StrEnum, auto


class TaskStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    UNKNOWN = auto()
