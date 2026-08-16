"""DI containers."""

from dependency_injector import containers, providers

from .use_cases import EventGenerator

WIRING_MODULES: list[str] = [
    '.entrypoints',
]


class Container(containers.DeclarativeContainer):
    """DI container."""

    wiring_config = containers.WiringConfiguration(modules=WIRING_MODULES)

    event_generator: providers.Factory[EventGenerator] = providers.Factory(
        EventGenerator,
    )
