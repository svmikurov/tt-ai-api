"""Abstract base classes."""

from abc import ABC, abstractmethod
from typing import Iterator


class AbstractEventGenerator(ABC):
    """ABC for event generator."""

    @abstractmethod
    def generate(self) -> Iterator[str]:
        """Generate the event."""
