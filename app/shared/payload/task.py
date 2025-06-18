from pydantic import BaseModel

from app.shared.enums.task_status import TaskStatus


class TaskResultResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: str | None = None
    error_code: str | None = None
    error_message: str | None = None


class TaskCreate(BaseModel):
    task_id: str
    file_id: int
    status: TaskStatus = TaskStatus.PENDING


class TaskUpdate(BaseModel):
    task_id: str
    file_id: int | None = None
    status: TaskStatus
