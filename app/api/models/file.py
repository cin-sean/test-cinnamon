from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db.database import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()
    total_pages: Mapped[int] = mapped_column()
