from io import BytesIO
from typing import Any

import requests

from app.shared.payload.infer import InferTaskResponse
from app.shared.settings import settings


class OCRService:
    def __init__(self):
        self.endpoint = settings.OCR_SERVICE_URL

    def infer(
        self,
        job_id: str,
        object_name: str,
        input_file: bytes,
        mimetype: str | None,
    ) -> InferTaskResponse:
        file_tuple: tuple[str, BytesIO, str] = (
            object_name,
            BytesIO(input_file),
            mimetype or "application/octet-stream",
        )
        files: dict[str, Any] = {"input": file_tuple}
        data = {"job_id": job_id}
        response = requests.post(
            f"{self.endpoint}/v2/ai/infer", data=data, files=files
        )

        response.raise_for_status()
        return InferTaskResponse(**response.json())
