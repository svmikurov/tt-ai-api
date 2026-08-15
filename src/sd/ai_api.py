"""AI API — синхронный сервис для обработки ML-запросов."""

import asyncio
import logging
import random
import time

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Семафор ограничивает одновременную обработку одним запросом
semaphore = asyncio.Semaphore(1)
app = FastAPI(title='AI API')


class PredictRequest(BaseModel):
    """Схема запроса к модели."""

    query: str


@app.middleware('http')
async def limit_requests(request: Request, call_next):
    """Middleware для ограничения количества одновременных запросов.

    Если семафор занят — возвращает 429 Too Many Requests.
    """
    if semaphore.locked():
        logger.warning('Request rejected: model busy')
        return Response(
            content='{"error": "Model is busy. Please try again later."}',
            status_code=429,
            media_type='application/json',
        )
    async with semaphore:
        logger.info('Request accepted')
        return await call_next(request)


@app.post('/predict')
def predict(request: PredictRequest):
    """Синхронный эндпоинт предсказания.

    1 запрос → 1 ответ. Остальные запросы отбрасываются (429).
    """
    logger.info(f'Processing: {request.query[:50]}...')
    delay = random.uniform(2.0, 4.0)
    time.sleep(delay)  # Имитация синхронной работы модели
    return {
        'result': f'Processed: {request.query}',
        'processing_time': delay,
        'model': 'sync-ai-model',
    }


@app.get('/health')
def health():
    """Проверка состояния сервиса."""
    return {'status': 'ok'}


@app.get('/metrics')
def metrics():
    """Метрики для мониторинга состояния модели."""
    return {
        'model': 'sync-ai-model',
        'busy': semaphore.locked(),
        'max_concurrent_requests': 1,
    }
