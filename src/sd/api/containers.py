"""DI containers."""

from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):
    """DI container."""

    config = providers.Configuration()
    config.redis.url = 'redis://localhost:6379'
    config.rabbit.url = 'amqp://guest:guest@localhost/'

    redis_service = providers.Singleton(
        services.RedisService,
        url=config.redis.url,
    )

    rabbit_service = providers.Singleton(
        services.RabbitMQService,
        url=config.rabbit.url,
    )

    task_service = providers.Factory(
        services.TaskService,
        redis_service=redis_service,
        rabbit_service=rabbit_service,
    )
