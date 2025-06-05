from enum import Enum

class WorkerQueue(str, Enum):
    ADD = "add_queue"
    SUBTRACT = "subtract_queue"
    MULTIPLY = "multiply_queue"
    DIVIDE = "divide_queue"
