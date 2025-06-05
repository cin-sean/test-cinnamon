from celery import Celery

from app.api.enums.task_name import TaskName
from app.api.enums.worker_queue import WorkerQueue

broker_url ="amqp://admin:cinnamon@rabbitmq:5672//"
redis_url = "redis://redis:6379/0"
celery_consumer = Celery('tasks', broker=broker_url, backend=redis_url)

@celery_consumer.task(name=TaskName.ADD, queue=WorkerQueue.ADD)
def add(a: float, b: float):
    return a + b

@celery_consumer.task(name=TaskName.SUBTRACT, queue=WorkerQueue.SUBTRACT)
def subtract(a: float, b: float):
    return a - b

@celery_consumer.task(name=TaskName.MULTIPLY, queue=WorkerQueue.MULTIPLY)
def multiply(a: float, b: float):
    return a * b

@celery_consumer.task(name=TaskName.DIVIDE, queue=WorkerQueue.DIVIDE)
def divide(a: float, b: float):
    return a / b

@celery_consumer.task(name=TaskName.XSUM, queue=WorkerQueue.ADD)
def xsum(arr: list[float]):
    return sum(arr)
