"""DI containers."""

from dependency_injector import containers, providers

from .sse_generators import SSEGenerator


class Container(containers.DeclarativeContainer):
    """DI container."""

    wiring_config = containers.WiringConfiguration(modules=['.entrypoints'])

    sse_generator = providers.Factory(SSEGenerator)
