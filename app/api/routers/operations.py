import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.celery_client import celery_client
from app.api.utils.ast_utils import extract_expression
from app.shared.enums.operation_type import OperationType
from app.shared.enums.task_name import TaskName
from app.shared.enums.task_status import TaskStatus
from app.shared.enums.worker_queue import WorkerQueue

logger = logging.getLogger(__name__)
logger.info("🧪 Inside FastAPI operations route logger!")
router = APIRouter()


class Param(BaseModel):
    a: int
    b: int


class XSumParam(BaseModel):
    arr: list[float]


class ExpressionParam(BaseModel):
    expression: str


class TaskResultResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: int | None = None
    error: str | None = None


# 4 endpoints for operation services
@router.post("/add")
def add(payload: Param) -> dict[str, str]:
    result = celery_client.send_task(
        TaskName.ADD, queue=WorkerQueue.ADD_QUEUE, kwargs=payload.model_dump()
    )
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


@router.post("/subtract")
def subtract(payload: Param) -> dict[str, str]:
    result = celery_client.send_task(
        TaskName.SUBTRACT,
        queue=WorkerQueue.SUBTRACT_QUEUE,
        kwargs=payload.model_dump(),
    )
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


@router.post("/multiply")
def multiply(payload: Param) -> dict[str, str]:
    result = celery_client.send_task(
        TaskName.MULTIPLY,
        queue=WorkerQueue.MULTIPLY_QUEUE,
        kwargs=payload.model_dump(),
    )
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


@router.post("/divide")
def divide(payload: Param) -> dict[str, str]:
    result = celery_client.send_task(
        TaskName.DIVIDE,
        queue=WorkerQueue.DIVIDE_QUEUE,
        kwargs=payload.model_dump(),
    )
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


# chaining mutable tasks
@router.post("/mutable")
def mutable(payload: ExpressionParam) -> dict[str, str]:
    expr = extract_expression(payload.expression, OperationType.MUTABLE)
    logger.info("extracted expression: %s", expr.task_id)
    result = expr.apply_async()
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


# chaining immutable tasks
@router.post("/immutable")
def immutable(payload: ExpressionParam) -> dict[str, str]:
    expr = extract_expression(payload.expression, OperationType.IMMUTABLE)
    logger.info("extracted expression: %s", expr)
    result = expr.apply_async()
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


# total using chord
@router.post("/chord")
def chord(payload: ExpressionParam) -> dict[str, str]:
    expr = extract_expression(payload.expression, OperationType.CHORD)
    logger.info("extracted expression: %s", expr)
    result = expr.apply_async()
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


# shorthand chaining
@router.post("/shorthand-chaining")
def shorthand_chaining(payload: ExpressionParam) -> dict[str, str]:
    expr = extract_expression(
        payload.expression, OperationType.SHORTHAND_CHAINING
    )
    logger.info("extracted expression: %s", expr)
    result = expr.apply_async()
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


# chord with callback
@router.post("/chord-with-callback")
def chord_with_callback(payload: ExpressionParam) -> dict[str, str]:
    result = extract_expression(
        payload.expression, OperationType.CHORD_WITH_CALLBACK
    )
    logger.info("task_id: %s", result.id)
    return {"task_id": result.id}


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str) -> TaskResultResponse:
    result = celery_client.AsyncResult(task_id)
    if result.ready():
        if result.successful():
            return TaskResultResponse(
                task_id=task_id,
                status=TaskStatus.SUCCESS,
                result=result.result,
            )
        else:
            return TaskResultResponse(
                task_id=task_id,
                status=TaskStatus.FAILURE,
                error=str(result.result),
            )
    else:
        return TaskResultResponse(
            task_id=task_id,
            status=result.state,
        )
