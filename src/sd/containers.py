"""Dependency injection containers."""

from dependency_injector import containers, providers

from .abstract import AbstractTaskProducer
from .celery_producer import CeleryTaskProducer
from .use_cases import GetResultUseCase, SendQuestionUseCase


class Container(containers.DeclarativeContainer):
    """DI контейнер для всего приложения."""

    wiring_config = containers.WiringConfiguration(modules=['.entrypoints'])

    task_producer: providers.Factory[AbstractTaskProducer] = providers.Factory(
        CeleryTaskProducer
    )

    send_prediction_use_case = providers.Factory(
        SendQuestionUseCase,
        task_producer=task_producer,
    )

    get_result_use_case = providers.Factory(
        GetResultUseCase,
        task_producer=task_producer,
    )
