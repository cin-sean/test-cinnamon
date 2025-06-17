from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.handlers.file.factory import FileHandlerFactory
from app.api.payload.file import UploadedFileCreate, UploadedFileResponse
from app.api.repos.file import UploadedFileRepo


class FileService:
    def __init__(self, db: Session):
        self.repo = UploadedFileRepo(db)

    def save_file(
        self,
        file: UploadFile,
        file_content: bytes,
        upload_file_create: UploadedFileCreate,
    ) -> UploadedFileResponse:
        # Validate and count pages
        handler = FileHandlerFactory.get_handler(file, file_content)
        handler.validate()
        total_pages = handler.get_page_count()

        if total_pages <= 0:
            raise ValueError("File must contain at least one page")

        record = self.repo.create_file(
            UploadedFileCreate(
                file_name=upload_file_create.file_name,
                file_path=upload_file_create.file_path,
                total_pages=total_pages,
            )
        )
        return UploadedFileResponse(
            id=record.id,
            file_name=record.file_name,
            total_pages=record.total_pages,
        )
