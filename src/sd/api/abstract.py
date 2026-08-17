"""Abstract base classes."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generic, TypeVar

RequestT = TypeVar('RequestT')
EventT = TypeVar('EventT')


class AbstractSSEGenerator(ABC, Generic[RequestT, EventT]):
    """ABC for SSE generator."""

    @abstractmethod
    def generate(self, request: RequestT) -> AsyncGenerator[EventT, None]:
        """Generate SSE events."""
