from fastapi import APIRouter
from pydantic import BaseModel

from app.api.celery_client import celery_client
from app.api.enums.operation_type import OperationType
from app.api.enums.task_name import TaskName
from app.api.enums.worker_queue import WorkerQueue
from app.api.utils.ast_utils import extract_expression

router = APIRouter()

class Param(BaseModel):
    a: int
    b: int

class XSumParam(BaseModel):
    arr: list[float]

class ExpressionParam(BaseModel):
    expression: str

# 4 endpoints for operation services
@router.post("/add")
def add(data: Param):
    result = celery_client.send_task(TaskName.ADD, queue=WorkerQueue.ADD, kwargs=dict(data))
    print({"task_id": result.id})
    return result.get(timeout=5)

@router.post("/subtract")
def subtract(data: Param):
    result = celery_client.send_task(TaskName.SUBTRACT, queue=WorkerQueue.SUBTRACT, kwargs=dict(data))
    print({"task_id": result.id})
    return result.get(timeout=5)

@router.post("/multiply")
def multiply(data: Param):
    result = celery_client.send_task(TaskName.MULTIPLY, queue=WorkerQueue.MULTIPLY, kwargs=dict(data))
    print({"task_id": result.id})
    return result.get(timeout=5)

@router.post("/divide")
def divide(data: Param):
    result = celery_client.send_task(TaskName.DIVIDE, queue=WorkerQueue.DIVIDE, kwargs=dict(data))
    print({"task_id": result.id})
    return result.get(timeout=5)

# chaining mutable tasks
@router.post("/mutable")
def mutable(data: ExpressionParam):
    expr = extract_expression(data.expression, OperationType.MUTABLE)
    print(expr)
    result = expr.apply_async()
    print({"task_id": result.id})
    return result.get(timeout=5)

# chaining immutable tasks
@router.post("/immutable")
def immutable(data: ExpressionParam):
    expr = extract_expression(data.expression, OperationType.IMMUTABLE)
    print(expr)
    result = expr.apply_async()
    print({"task_id": result.id})
    return result.get(timeout=5)

# total using chord
@router.post("/chord")
def chord(data: ExpressionParam):
    expr = extract_expression(data.expression, OperationType.CHORD)
    print(expr)
    result = expr.apply_async()
    print({"task_id": result.id})
    return result.get(timeout=5)

# shorthand chaining
@router.post("/shorthand-chaining")
def shorthand_chaining(data: ExpressionParam):
    expr = extract_expression(data.expression, OperationType.SHORTHAND_CHAINING)
    print(expr)
    result = expr.apply_async()
    print({"task_id": result.id})
    return result.get(timeout=5)

# chord with callback
@router.post("/chord-with-callback")
def chord(data: ExpressionParam):
    result = extract_expression(data.expression, OperationType.CHORD_WITH_CALLBACK)
    print({"task_id": result.id})
    return result.get(timeout=5)
