from fastapi import UploadFile

from app.api.handlers.file.base_file_handler import BaseFileHandler
from app.api.handlers.file.image_handler import ImageHandler
from app.api.handlers.file.pdf_handler import PDFHandler
from app.shared.enums.file_extension import FileExtension


class FileHandlerFactory:
    @staticmethod
    def get_handler(file: UploadFile, content: bytes) -> BaseFileHandler:
        ext = file.filename.lower().split(".")[-1]

        if ext == FileExtension.PDF:
            return PDFHandler(file, content)
        elif ext in [FileExtension.JPG, FileExtension.PNG, FileExtension.TIFF]:
            return ImageHandler(file, content)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
