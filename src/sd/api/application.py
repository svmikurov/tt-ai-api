"""Applicatio factory module."""

from fastapi import FastAPI

from sd.api import entrypoints
from sd.api.containers import Container


async def lifespan(app: FastAPI):
    """Lifecycle management through a container."""
    await app.container.redis_service().connect()
    await app.container.rabbit_service().connect()

    yield

    await app.container.rabbit_service().close()
    await app.container.redis_service().close()


def create_app() -> FastAPI:
    """Create API application."""
    container = Container()

    app = FastAPI(lifespan=lifespan)

    app.container = container

    app.include_router(entrypoints.router)

    return app


app = create_app()
