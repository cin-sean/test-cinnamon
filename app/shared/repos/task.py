from sqlalchemy.orm import Session

from app.shared.models.task import Task
from app.shared.payload.task import TaskCreate, TaskUpdate


class TaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_create: TaskCreate) -> Task:
        new_task = Task(
            task_id=task_create.task_id,
            file_id=task_create.file_id,
            status=task_create.status,
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update_task(self, task_update: TaskUpdate) -> Task | None:
        task = (
            self.db.query(Task)
            .filter(Task.task_id == task_update.task_id)
            .first()
        )
        if not task:
            return None
        task.status = task_update.status
        self.db.commit()
        self.db.refresh(task)
        return task
