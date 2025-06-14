from enum import StrEnum, auto

class TaskName(StrEnum):
    INFER = auto()
    PROCESS_PAGE = auto()
    FINALIZE_TASK = auto()
