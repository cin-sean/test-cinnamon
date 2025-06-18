import time

from fastapi import UploadFile


class FileUtils:
    @staticmethod
    def generate_unique_name(file: UploadFile) -> str:
        ts = int(time.time() * 1000)
        ext = file.filename.split(".")[-1]
        file_name = file.filename.split(".")[0]
        return f"{file_name}-{ts}.{ext}"

    @staticmethod
    def get_file_extension(file: UploadFile) -> str:
        return file.filename.split(".")[-1]
