from PIL import Image
from io import BytesIO

from app.api.handlers.file.base_file_handler import BaseFileHandler
from app.shared.enums.file_extension import FileExtension

class ImageHandler(BaseFileHandler):
    def validate(self):
        ext = self.file.filename.lower().split(".")[-1]
        if ext not in [FileExtension.JPG, FileExtension.PNG, FileExtension.TIFF]:
            raise ValueError("Invalid Invalid image file type")

    def get_page_count(self) -> int:
        ext = self.file.filename.lower().split(".")[-1]
        if ext in [FileExtension.JPG, FileExtension.PNG]:
            return 1
        elif ext == FileExtension.TIFF:
            img = Image.open(BytesIO(self.content))
            count = 0
            try:
                while True:
                    img.seek(count)
                    count += 1
            except EOFError:
                return count
        return 0