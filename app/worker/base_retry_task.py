import logging
from typing import Any

from celery import Task
from celery.exceptions import SoftTimeLimitExceeded

from app.worker.settings import settings as worker_settings

logger = logging.getLogger(__name__)


class BaseRetryTask(Task):
    autoretry_for = (SoftTimeLimitExceeded,)
    retry_kwargs = {
        "max_retries": worker_settings.MAX_RETRIES,
        "countdown": worker_settings.RETRY_DELAY,
    }

    def on_retry(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Exception,
    ) -> None:
        logger.warning(
            "🔁 [RETRY] Task %s will retry due to %s: %s",
            task_id,
            type(exc).__name__,
            exc,
        )

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Exception,
    ) -> None:
        logger.error(
            "❌ [FAILURE] Task %s failed permanently.\n"
            "Exception: %s: %s\n"
            "Args: %s\nKwargs: %s",
            task_id,
            type(exc).__name__,
            args,
            kwargs,
        )
