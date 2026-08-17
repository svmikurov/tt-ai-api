"""Schemas."""

from pydantic import BaseModel

from .enums import SSEvent
from .types import TypedPredictResult


class PredictRequest(BaseModel):
    """Predict request schema."""

    query: str


class PredictResult(BaseModel):
    """Predict result schema."""

    answer: str


class PredictSSE(BaseModel):
    """Predict SSE response schema."""

    event: SSEvent
    data: TypedPredictResult
