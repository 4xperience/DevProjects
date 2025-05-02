from celery import Celery
from src.core.config import settings

celery_app = Celery(
    "delivery_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.tasks"]
)

celery_app.conf.enable_utc = True
celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "calc-delivery-every-5-min": {
        "task": "src.tasks.calculate_delivery_cost",
        "schedule": 300
    }
}
