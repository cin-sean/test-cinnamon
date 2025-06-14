from pydantic import BaseModel

class FileCreate(BaseModel):
    file_name: str
    total_pages: int

class FileResponse(FileCreate):
    id: int

    class Config:
        orm_mode = True
