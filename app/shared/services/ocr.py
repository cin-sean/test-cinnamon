from app.shared.payload.infer import InferTaskResponse
from app.shared.settings import settings
import requests

class OCRService:
    def __init__(self):
        self.endpoint = settings.OCR_SERVICE_URL

    def infer(self, job_id: str, object_name: str, input_file: bytes, mimetype: str) -> InferTaskResponse:
        files = {"input": (object_name, input_file, mimetype)}
        data = {"job_id": job_id}
        response = requests.post(f"{self.endpoint}/v2/ai/infer", data=data, files=files)

        response.raise_for_status()
        return response.json()