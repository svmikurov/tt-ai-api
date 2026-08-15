"""Redis produser."""

import json
import os
import uuid
from typing import Any, Dict

import redis

from .abstract import AbstractTaskProducer


class RedisTaskProducer(AbstractTaskProducer):
    """Реализация через Redis напрямую (без Celery)."""

    def __init__(self, redis_url: str | None = None) -> None:
        redis_url = redis_url or os.getenv(
            'REDIS_URL', 'redis://localhost:6379/0'
        )
        self._client = redis.from_url(redis_url)

    def send_task(self, query: str) -> str:
        """Отправить задачу и вернуть task_id."""
        task_id = str(uuid.uuid4())

        task_data = {
            'task_id': task_id,
            'query': query,
            'status': 'queued',
        }

        # Отправляем в очередь
        self._client.rpush('tasks', json.dumps(task_data))

        # Сохраняем статус
        self._client.setex(
            f'status:{task_id}',
            3600,
            json.dumps({'status': 'queued'}),
        )

        return task_id

    def get_result(self, task_id: str) -> Dict[str, Any] | None:
        """Получить результат по task_id."""
        result_data = self._client.get(f'result:{task_id}')

        if result_data:
            return json.loads(result_data)
        return None

    def get_status(self, task_id: str) -> str:
        """Получить статус задачи."""
        status_data = self._client.get(f'status:{task_id}')

        if not status_data:
            return 'not found'

        status = json.loads(status_data)
        return status.get('status', 'unknown')
