from enum import StrEnum, auto

class WorkerQueue(StrEnum):
    ADD_QUEUE = auto()
    SUBTRACT_QUEUE = auto()
    MULTIPLY_QUEUE = auto()
    DIVIDE_QUEUE = auto()
