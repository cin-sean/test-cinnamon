from enum import StrEnum, auto


class TaskStatus(StrEnum):
    SUCCESS = auto()
    FAILURE = auto()
    TIMEOUT = auto()
    ERROR = auto()
