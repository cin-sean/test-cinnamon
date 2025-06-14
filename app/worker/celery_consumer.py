import json
import logging
import mimetypes
from io import BytesIO

from celery import Celery, current_task, chord

from app.shared.db.database import get_db
from app.shared.enums.folder import Folder
from app.shared.enums.task_status import TaskStatus
from app.shared.payload.infer import InferTaskResponse
from app.shared.payload.task import TaskUpdate
from app.shared.services.ocr import OCRService
from app.shared.enums.task_name import TaskName
from app.shared.enums.worker_queue import WorkerQueue
from app.shared.services.storage import StorageService, get_object_name, get_file_name
from app.shared.services.task import TaskService
from app.shared.settings import settings
from app.worker.settings import settings as worker_settings
from app.worker.base_retry_task import BaseRetryTask

celery_consumer = Celery('tasks', broker=settings.BROKER_URL, backend=settings.REDIS_URL)
logger = logging.getLogger(__name__)

@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.INFER,
    queue=WorkerQueue.OCR_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def ocr_process(file_path: str) -> dict:
    task_id = current_task.request.id
    task_service = TaskService(next(get_db()))

    try:
        task_service.update_task(TaskUpdate(task_id=task_id, status=TaskStatus.PROCESSING))

        object_name = get_object_name(file_path)
        file_name = get_file_name(file_path).split(".")[0]

        storage_service = StorageService()
        file_content = storage_service.download_file(file_path)
        mimetype, _ = mimetypes.guess_type(object_name)

        ocr_service = OCRService()
        response = ocr_service.infer(task_id, object_name, file_content, mimetype)

        # Simulate an error response for testing
        # response = {
        #               "job_id": "1",
        #               "metadata": {
        #                 "version": "1.9.0",
        #                 "product_line": "flax"
        #               },
        #               "error_code": "E10007",
        #               "error_message": "Unsupported file extension: .txt",
        #               "result": [],
        #               "result_by_file": {}
        #             }

        if response.get("error_code") and response.get("error_message"):
            raise Exception(json.dumps({
                'error_code': response.get("error_code"),
                'error_message': response.get("error_message"),
            }))

        result_pages = response.get("result", {})
        result_by_file = response.get("result_by_file", {})
        header = [process_page.s(task_id, file_name, page_content, idx + 1) for idx, page_content in enumerate(result_pages)]
        chord(header)(finalize_task.s(task_id))

        return InferTaskResponse(
            job_id=task_id,
            result=result_pages,
            result_by_file=result_by_file
        ).model_dump()
    except Exception as e:
        logger.error(f"❌ Error in ocr_process task {task_id}, {e}")
        task_service.update_task(TaskUpdate(task_id=task_id, status=TaskStatus.FAILED))
        raise e

@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.PROCESS_PAGE,
    queue=WorkerQueue.OCR_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def process_page(task_id, file_name, page_content, page_num) -> dict:
    # store JSON page content in MinIO
    storage_service = StorageService()
    task_service = TaskService(next(get_db()))
    json_bytes = BytesIO(json.dumps(page_content).encode('utf-8'))
    page_file_name = f"{file_name}_{page_num}.json"

    try:
        file_path = storage_service.upload_file(
            file=json_bytes,
            saved_file_name=page_file_name,
            folder=Folder.OCR,
            content_type="application/json"
        )
    except Exception as e:
        logger.error(f"❌ Error in process_page task {task_id}, {e}")
        task_service.update_task(TaskUpdate(task_id=task_id, status=TaskStatus.FAILED))
        raise e

    return {
        "task_id": task_id,
        "file_path": file_path,
        "page_num": page_num
    }

@celery_consumer.task(
    base=BaseRetryTask,
    name=TaskName.FINALIZE_TASK,
    queue=WorkerQueue.OCR_QUEUE,
    soft_time_limit=worker_settings.SOFT_TIME_LIMIT,
)
def finalize_task(header_results, task_id) -> None:
    task_service = TaskService(next(get_db()))
    task_service.update_task(TaskUpdate(task_id=task_id, status=TaskStatus.COMPLETED))
