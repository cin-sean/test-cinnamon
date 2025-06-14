from fastapi import UploadFile

class BaseFileHandler:
    def __init__(self, file: UploadFile, content: bytes):
        self.file = file
        self.content = content

    def validate(self):
        raise NotImplementedError

    def get_page_count(self) -> int:
        raise NotImplementedError