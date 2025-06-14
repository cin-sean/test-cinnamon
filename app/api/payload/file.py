from pydantic import BaseModel

class UploadedFileCreate(BaseModel):
    file_name: str = ""
    file_path: str = ""
    total_pages: int = 0

class UploadedFileResponse(BaseModel):
    id: int
    file_name: str = ""
    total_pages: int = 0
