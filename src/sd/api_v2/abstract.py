"""Abstract base classes."""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator


class AbstractTaskProducer(ABC):
    """ABC for sending tasks to broker."""

    @abstractmethod
    async def send_task(
        self,
        task_id: str,
        query: str,
    ) -> AsyncGenerator[None, None]:
        """Send the task to the queue for execution."""

    @abstractmethod
    def get_result(self, task_id: str) -> dict[str, Any] | None:
        """Get result by task_id."""

    @abstractmethod
    def get_status(self, task_id: str) -> str:
        """Get task status."""


class AbstractResultStorage(ABC):
    """ABC for tak result storage."""

    @abstractmethod
    def listen(self, task_id: str) -> AsyncGenerator[str, None]:
        """Listen the events."""
