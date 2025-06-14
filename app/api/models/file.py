from sqlalchemy import Column, Integer, String

from app.shared.db.database import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    total_pages = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
