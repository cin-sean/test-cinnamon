from sqlalchemy.orm import Session

from app.api.models.file import UploadedFile
from app.api.payload.file import UploadedFileCreate, UploadedFileResponse


class UploadedFileRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_file(self, uploaded_file_create: UploadedFileCreate) -> UploadedFile:
        db_obj = UploadedFile(**uploaded_file_create.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_file(self, file_id: int) -> UploadedFile | None:
        return self.db.query(UploadedFile).filter(UploadedFile.id == file_id).first()