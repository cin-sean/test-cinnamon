import json

from fastapi import APIRouter

from app.api.celery_client import celery_client
from app.shared.enums.celery_task_status import CeleryTaskStatus
from app.shared.payload.task import TaskResultResponse
from app.shared.enums.task_status import TaskStatus

router = APIRouter()

@router.get("/{task_id}")
def get_task_status(task_id: str):
    result = celery_client.AsyncResult(task_id)
    if result.state == CeleryTaskStatus.PENDING:
        return TaskResultResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
        )

    if result.state == CeleryTaskStatus.STARTED or result.state == CeleryTaskStatus.RETRY:
        return TaskResultResponse(
            task_id=task_id,
            status=TaskStatus.PROCESSING,
        )

    if result.state == CeleryTaskStatus.SUCCESS:
        return TaskResultResponse(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            result=json.dumps(result.result)
        )

    if result.state == CeleryTaskStatus.FAILURE:
        error = result.result
        try:
            error_data = json.loads(str(error))
            return TaskResultResponse(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error_code=error_data.get('error_code'),
                error_message=error_data.get('error_message'),
            )
        except json.JSONDecodeError:
            return TaskResultResponse(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error_message=str(error)
            )

    return TaskResultResponse(
        task_id=task_id,
        status=TaskStatus.UNKNOWN,
        error_message="Unhandled task state"
    )