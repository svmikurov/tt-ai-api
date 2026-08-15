"""API enumerations."""

from enum import Enum


class SSEvent(Enum):
    """Send Server Event enumeration."""

    CREATED = 'created'
    PROGRESS = 'progress'
    RESULT = 'result'
    ERROR = 'error'
    COMPLETE = 'complete'


class TaskStatus(Enum):
    """Task status enumeration."""

    QUEUED = 'queued'
