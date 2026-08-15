"""FastAPI entrypoint."""

from fastapi import FastAPI
from sqlalchemy import create_engine, text
import redis
import os
from sd.infrastructure.broker.tasks import process_ml_request

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://user:password@db:5432/demo')
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = FastAPI(title='Demo API', version='0.1.0')
engine = create_engine(DATABASE_URL)
redis_client = redis.from_url(REDIS_URL)

@app.get('/')
async def root():
    return {'message': 'Hello FastAPI!'}


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.get('/db-check')
async def db_check():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        return {"status": "connected", "result": result.scalar()}


@app.get('/redis-check')
async def redis_check():
    redis_client.set("test_key", "test_value")
    value = redis_client.get("test_key")
    return {"status": "connected", "value": value.decode()}


@app.post("/predict")
async def predict(query: dict):
    """Отправка задачи в очередь"""
    task = process_ml_request.delay(query)
    return {
        "task_id": task.id,
        "status": "queued",
        "message": "Task sent to ML worker"
    }

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    """Получение результата по task_id"""
    # Проверяем статус задачи
    task = process_ml_request.AsyncResult(task_id)
    
    if task.ready():
        return {
            "task_id": task_id,
            "status": "completed",
            "result": task.get()
        }
    else:
        return {
            "task_id": task_id,
            "status": "pending",
            "message": "Task is still processing"
        }