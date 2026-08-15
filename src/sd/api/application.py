"""Application module."""

from fastapi import FastAPI

from . import entrypoints


def create_app() -> FastAPI:
    """Create API application."""
    app = FastAPI()

    app.include_router(entrypoints.router)

    return app


app = create_app()
