"""Celery produser."""

from typing import Any, Dict

from .abstract import AbstractTaskProducer
from .tasks import process_ml_request


class CeleryTaskProducer(AbstractTaskProducer):
    """Реализация через Celery."""

    def send_task(self, query: str) -> str:
        """Отправить задачу и вернуть task_id."""
        task = process_ml_request.delay({'query': query})
        return task.id

    def get_result(self, task_id: str) -> Dict[str, Any] | None:
        """Получить результат по task_id."""
        task = process_ml_request.AsyncResult(task_id)
        if task.ready():
            return task.get()
        return None

    def get_status(self, task_id: str) -> str:
        """Получить статус задачи."""
        task = process_ml_request.AsyncResult(task_id)
        if task.ready():
            return 'completed'
        return 'pending'
