# src/sd/entrypoints/main.py
"""FastAPI entrypoint.

Этот модуль является точкой входа для HTTP API сервиса.
Он обрабатывает входящие запросы, делегирует бизнес-логику Use Cases
и возвращает ответы клиентам.
"""

import os
from typing import Annotated

import redis
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy import create_engine, text

from .containers import Container
from .use_cases import GetResultUseCase, SendQuestionUseCase

# ============================================================
# Инициализация
# ============================================================

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://user:password@db:5432/demo'
)
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

router = APIRouter()
engine = create_engine(DATABASE_URL)
redis_client = redis.from_url(REDIS_URL)


# ============================================================
# Health Checks
# ============================================================


@router.get('/')
async def root():
    """Корневой эндпоинт для проверки доступности сервиса."""
    return {'message': 'Hello FastAPI!'}


@router.get('/health')
async def health():
    """Проверка состояния сервиса."""
    return {'status': 'ok'}


@router.get('/db-check')
async def db_check():
    """Проверка подключения к PostgreSQL.

    Returns:
        dict: Статус подключения и результат тестового запроса.

    """
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        return {'status': 'connected', 'result': result.scalar()}


@router.get('/redis-check')
async def redis_check():
    """Проверка подключения к Redis.

    Returns:
        dict: Статус подключения и значение тестового ключа.

    """
    try:
        redis_client.set('test_key', 'test_value')
        value = redis_client.get('test_key')
        return {'status': 'connected', 'value': value.decode()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# ============================================================
# Основные бизнес-эндпоинты
# ============================================================


@router.post('/predict')
@inject
async def predict(
    query: dict,
    use_case: Annotated[
        SendQuestionUseCase,
        Depends(Provide[Container.send_prediction_use_case]),
    ],
):
    """Отправка запроса на предсказание в очередь задач.

    Returns:
        dict: task_id, статус и сообщение о постановке задачи в очередь.

    Example:
        >>> POST /predict {"query": "Привет, нейросеть!"}
        {
            "task_id": "abc-123",
            "status": "queued",
            "message": "Task sent to ML worker"
        }

    """
    return use_case.execute(query.get('query', ''))


@router.get('/result/{task_id}')
@inject
async def get_result(
    task_id: str,
    use_case: Annotated[
        GetResultUseCase, Depends(Provide[Container.get_result_use_case])
    ],
):
    """Получение результата обработки задачи по её task_id.

    Returns:
        dict: Статус задачи и результат (если завершена).

    Example:
        >>> GET /result/abc-123
        {
            "task_id": "abc-123",
            "status": "completed",
            "result": {"status": "completed", ...}
        }

    Возможные статусы:
        - pending: задача ещё выполняется
        - completed: задача завершена, результат доступен
        - not_found: задача не найдена (или результат удалён)

    """
    return use_case.execute(task_id)
