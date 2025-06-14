from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
from app.worker.settings import settings as worker_settings
import logging

logger = logging.getLogger(__name__)

class BaseRetryTask(Task):
    autoretry_for = (SoftTimeLimitExceeded,)
    retry_kwargs = {
        'max_retries': worker_settings.MAX_RETRIES,
        'countdown': worker_settings.RETRY_DELAY
    }

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(
            f"🔁 [RETRY] Task {task_id} will retry due to {type(exc).__name__}: {exc}"
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(
            f"❌ [FAILURE] Task {task_id} failed permanently.\n"
            f"Exception: {type(exc).__name__}: {exc}\n"
            f"Args: {args}\nKwargs: {kwargs}"
        )