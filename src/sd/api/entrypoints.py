"""Entrypoints."""

from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from .abstract import AbstractSSEGenerator
from .containers import Container
from .schemas import PredictRequest
from .types import TypedSSEvent

router = APIRouter()


@router.post('/predict')
@inject
def predict(
    request: PredictRequest,
    sse_generator: Annotated[
        AbstractSSEGenerator[PredictRequest, TypedSSEvent],
        Depends(Provide[Container.sse_generator]),
    ],
) -> EventSourceResponse:
    """Stream events."""
    return EventSourceResponse(sse_generator.generate(request))
