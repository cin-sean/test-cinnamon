import os
from typing import IO, Optional, Union

from starlette.datastructures import UploadFile

from app.shared.enums.bucket import Bucket
from app.shared.fs_client import fs_client


def get_object_name(file_path: str) -> str:
    if not file_path.startswith(f"{Bucket.UPLOADED_FILES}/"):
        raise ValueError(f"Invalid file path: {file_path}")
    return file_path[len(f"{Bucket.UPLOADED_FILES}/") :]


def get_file_name(file_path: str) -> str:
    object_name = get_object_name(file_path)
    return os.path.basename(object_name)


class StorageService:
    def __init__(self):
        self.fs_client = fs_client
        # Ensure default buckets exist
        if not self.fs_client.bucket_exists(Bucket.UPLOADED_FILES):
            self.fs_client.make_bucket(Bucket.UPLOADED_FILES)

    def upload_file(
        self,
        file: Union[UploadFile, IO[bytes]],
        saved_file_name: str,
        folder: str = "",
        content_type: Optional[str] = None,
    ) -> str:
        object_name = os.path.join(folder, saved_file_name).replace("\\", "/")
        if isinstance(file, UploadFile):
            file_obj = file.file
            content_type = content_type or file.content_type
        else:
            file_obj = file
            content_type = content_type or "application/octet-stream"

        # Get file size
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)

        self.fs_client.put_object(
            bucket_name=Bucket.UPLOADED_FILES,
            object_name=object_name,
            data=file_obj,
            length=file_size,
            content_type=content_type,
        )

        return f"{Bucket.UPLOADED_FILES}/{object_name}"

    def download_file(self, file_path: str) -> bytes:
        object_name = get_object_name(file_path)
        try:
            response = self.fs_client.get_object(
                Bucket.UPLOADED_FILES, object_name
            )
            return response.read()
        except Exception as e:
            raise FileNotFoundError(
                f"File not found: {object_name}. Error: {str(e)}"
            )
