"""Tasks."""

import time
import os
import requests
from celery import Celery

celery_app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

AI_API_URL = os.getenv("AI_API_URL", "http://ai-api:8001/predict")

@celery_app.task
def process_ml_request(data: dict):
    """Вызов синхронного AI API."""
    query = data.get('query', '')
    
    try:
        response = requests.post(
            AI_API_URL,
            json={"query": query},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "status": "completed",
                "result": result.get("result", "No result"),
                "processing_time": result.get("processing_time", 0),
                "model": result.get("model", "unknown"),
                "task_id": process_ml_request.request.id
            }
        else:
            return {
                "status": "failed",
                "error": f"AI API error: {response.status_code}",
                "task_id": process_ml_request.request.id
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "task_id": process_ml_request.request.id
        }