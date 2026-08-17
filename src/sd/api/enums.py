"""Enumerations."""

from enum import Enum


class SSEvent(str, Enum):
    """Send Server Event enumeration."""

    CREATED = 'created'
