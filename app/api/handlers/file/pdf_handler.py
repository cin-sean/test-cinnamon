from PyPDF2 import PdfReader
from io import BytesIO

from app.api.handlers.file.base_file_handler import BaseFileHandler
from app.shared.enums.file_extension import FileExtension


class PDFHandler(BaseFileHandler):
    def validate(self):
        ext = self.file.filename.lower().split(".")[-1]
        if ext != FileExtension.PDF:
            raise ValueError("Invalid file type for PDF handler")

    def get_page_count(self) -> int:
        reader = PdfReader(BytesIO(self.content))
        return len(reader.pages)