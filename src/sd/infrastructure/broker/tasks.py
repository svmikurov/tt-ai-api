"""Tasks."""

import time
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_ml_request(data: dict):
    """Имитация долгого синхронного вызова ML-API"""
    # Эмуляция работы модели 5–10 секунд
    time.sleep(5)
    return {
        "status": "completed",
        "result": f"Processed: {data.get('query', 'no query')}",
        "task_id": process_ml_request.request.id
    }