from enum import StrEnum


class CeleryTaskStatus(StrEnum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    RETRY = "RETRY"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
