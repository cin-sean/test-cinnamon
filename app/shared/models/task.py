from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    file_id: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
