import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.celery_client import celery_client
from app.api.payload.file import UploadedFileCreate
from app.api.services.file import FileService
from app.api.utils.file import FileUtils
from app.shared.db.database import get_db
from app.shared.enums.folder import Folder
from app.shared.enums.task_name import TaskName
from app.shared.enums.task_status import TaskStatus
from app.shared.enums.worker_queue import WorkerQueue
from app.shared.payload.infer import InferResponse
from app.shared.payload.task import TaskCreate
from app.shared.services.storage import StorageService
from app.shared.services.task import TaskService

logger = logging.getLogger(__name__)
logger.info("🧪 Inside FastAPI operations route logger!")
router = APIRouter()


@router.post("/infer")
async def infer(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        storage_service = StorageService()
        saved_file_name = FileUtils.generate_unique_name(file)
        file_path = storage_service.upload_file(
            file, saved_file_name, Folder.OCR
        )
        logger.info("✅ File saved to path: %s", file_path)

        file.file.seek(0)
        file_content = file.file.read()
        file_service = FileService(db)
        saved_file = file_service.save_file(
            file,
            file_content=file_content,
            upload_file_create=UploadedFileCreate(
                file_name=saved_file_name,
                file_path=file_path,
            ),
        )
        logger.info("✅ File metadata saved: %s", saved_file)

        task = celery_client.send_task(
            TaskName.INFER,
            queue=WorkerQueue.OCR_QUEUE,
            kwargs={"file_path": file_path},
        )
        logger.info("✅ Task sent to Celery: %s", task.id)

        task_service = TaskService(db)
        saved_task = task_service.create_task(
            TaskCreate(
                task_id=task.id,
                file_id=saved_file.id,
                status=TaskStatus.PENDING,
            )
        )
        logger.info("✅ Task metadata saved: %s", saved_task)

        return InferResponse(task_id=task.id)
    except Exception as e:
        logger.error(f"❌ Error in infer: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Test API for uploading file
@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    file_service = FileService(db)
    storage_service = StorageService()
    try:
        saved_file_name = FileUtils.generate_unique_name(file)
        file_content = file.file.read()
        result = file_service.save_file(
            file,
            file_content=file_content,
            upload_file_create=UploadedFileCreate(
                file_name=saved_file_name,
                file_path="/test",
            ),
        )
        logger.info("result: %s", result)
        path = storage_service.upload_file(file, result.file_name, Folder.OCR)
    except ValueError as e:
        logger.error(f"❌ Error reading file: {e}")
        raise HTTPException(status_code=400, detail="Invalid file content")
    return {"result": result, "path": path}
