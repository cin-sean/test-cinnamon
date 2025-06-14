from sqlalchemy import Column, Integer, String

from app.shared.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True, index=True)
    file_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)