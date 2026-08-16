"""API entrypoints."""

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from .abstract import AbstractEventGenerator
from .containers import Container

router = APIRouter()


@router.get('/process')
@inject
def process(
    query: str,
    event_generator: Annotated[
        AbstractEventGenerator,
        Depends(Provide[Container.event_generator]),
    ],
):
    """Process AI request."""
    return EventSourceResponse(
        event_generator.generate(),
        headers={
            'X-Accel-Buffering': 'no',
        },
    )
