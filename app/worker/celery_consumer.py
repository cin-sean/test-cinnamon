from celery import Celery

from app.shared.enums.task_name import TaskName
from app.shared.enums.worker_queue import WorkerQueue
from app.shared.settings import settings
from app.worker.base_retry_task import BaseRetryTask
from app.worker.settings import settings as worker_settings

celery_consumer = Celery(
    "tasks", broker=settings.BROKER_URL, backend=settings.REDIS_URL
)


@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.ADD,
    queue=WorkerQueue.ADD_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def add(a: float, b: float) -> float:
    return a + b


@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.SUBTRACT,
    queue=WorkerQueue.SUBTRACT_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def subtract(a: float, b: float) -> float:
    return a - b


@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.MULTIPLY,
    queue=WorkerQueue.MULTIPLY_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def multiply(a: float, b: float) -> float:
    return a * b


@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.DIVIDE,
    queue=WorkerQueue.DIVIDE_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.XSUM,
    queue=WorkerQueue.ADD_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def xsum(arr: list[float]) -> float:
    return sum(arr)
