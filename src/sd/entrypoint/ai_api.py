"""Синхронное AI API."""

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import time
import random
import asyncio

# Семафор на 1 одновременный запрос
semaphore = asyncio.Semaphore(1)

app = FastAPI(title="Synchronous AI API")

class PredictRequest(BaseModel):
    query: str

@app.middleware("http")
async def limit_requests(request: Request, call_next):
    if semaphore.locked():
        return Response(
            content='{"error": "Model is busy. Please try again later."}',
            status_code=429,
            media_type="application/json"
        )
    async with semaphore:
        return await call_next(request)

@app.post("/predict")
def predict(request: PredictRequest):
    """Синхронный эндпоинт. 1 запрос → 1 ответ."""
    delay = random.uniform(2.0, 4.0)
    time.sleep(delay)
    return {
        "result": f"Processed: {request.query}",
        "processing_time": delay,
        "model": "sync-ai-model"
    }

@app.get("/health")
def health():
    return {"status": "ok"}