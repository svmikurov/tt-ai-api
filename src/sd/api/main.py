"""Main."""

from fastapi import FastAPI

from . import entrypoints
from .containers import Container


def create_app() -> FastAPI:
    """Create API application."""
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore[attr-defined]
    app.include_router(entrypoints.router)
    return app


app = create_app()
