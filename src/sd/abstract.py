"""Abstract base classes."""

from abc import ABC, abstractmethod
from typing import Any


class AbstractTaskProducer(ABC):
    """Абстракция для отправки задач в брокер."""

    @abstractmethod
    def send_task(self, query: str) -> str:
        """Отправить задачу и вернуть task_id."""

    @abstractmethod
    def get_result(self, task_id: str) -> dict[str, Any] | None:
        """Получить результат по task_id."""

    @abstractmethod
    def get_status(self, task_id: str) -> str:
        """Получить статус задачи."""
