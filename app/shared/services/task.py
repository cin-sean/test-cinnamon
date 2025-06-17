from sqlalchemy.orm import Session

from app.shared.models.task import Task
from app.shared.payload.task import TaskCreate, TaskUpdate
from app.shared.repos.task import TaskRepo


class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepo(db)

    def create_task(self, task_create: TaskCreate) -> Task:
        return self.repo.create_task(task_create)

    def update_task(self, task_update: TaskUpdate) -> Task | None:
        return self.repo.update_task(task_update)
