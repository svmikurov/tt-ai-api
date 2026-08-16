"""Use cases."""

from typing import Iterator, override

from .abstract import AbstractEventGenerator


class EventGenerator(AbstractEventGenerator):
    """Event generator."""

    def __init__(self) -> None:
        pass

    @override
    def generate(self) -> Iterator[str]:
        """Generate event."""
        raise NotImplementedError('Implement event generator.')
