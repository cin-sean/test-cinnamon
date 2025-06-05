from celery import Celery

broker_url ="amqp://admin:cinnamon@rabbitmq:5672//"
redis_url = "redis://redis:6379/0"
celery_client = Celery('apis', broker=broker_url, backend=redis_url)
