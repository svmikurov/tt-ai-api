"""Types."""

from typing import TypedDict

from .enums import SSEvent


class TypedPredictResult(TypedDict):
    """Typed predict result."""

    answer: str


class TypedSSEvent(TypedDict):
    """Typed Send Server Event."""

    event: SSEvent
    data: TypedPredictResult
