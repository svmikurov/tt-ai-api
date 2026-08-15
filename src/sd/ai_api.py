"""AI API."""
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import time
import random
import asyncio
import logging

logger = logging.getLogger(__name__)

semaphore = asyncio.Semaphore(1)
app = FastAPI(title="AI API")

class PredictRequest(BaseModel):
    query: str

@app.middleware("http")
async def limit_requests(request: Request, call_next):
    if semaphore.locked():
        logger.warning("Request rejected: model busy")
        return Response(
            content='{"error": "Model is busy. Please try again later."}',
            status_code=429,
            media_type="application/json"
        )
    async with semaphore:
        logger.info("Request accepted")
        return await call_next(request)

@app.post("/predict")
def predict(request: PredictRequest):
    logger.info(f"Processing: {request.query[:50]}...")
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

@app.get("/metrics")
def metrics():
    return {
        "model": "sync-ai-model",
        "busy": semaphore.locked(),
        "max_concurrent_requests": 1
    }