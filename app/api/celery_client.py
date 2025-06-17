from celery import Celery

from app.shared.settings import settings

celery_client = Celery(
    "apis", broker=settings.BROKER_URL, backend=settings.REDIS_URL
)
