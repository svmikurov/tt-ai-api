"""SSE generators."""

from typing import AsyncGenerator

from .abstract import AbstractSSEGenerator
from .enums import SSEvent
from .schemas import PredictRequest
from .types import TypedSSEvent


class SSEGenerator(AbstractSSEGenerator[PredictRequest, TypedSSEvent]):
    """SSE generator."""

    async def generate(
        self,
        request: PredictRequest,
    ) -> AsyncGenerator[TypedSSEvent, None]:
        """Generate SSE events."""
        yield {
            'event': SSEvent.CREATED,
            'data': {'answer': 'answer'},
        }
