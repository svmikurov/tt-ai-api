import os
import logging
import requests
from celery import Celery
from celery.exceptions import Retry

logger = logging.getLogger(__name__)

celery_app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

AI_API_URL = os.getenv("AI_API_URL", "http://ai-api:8001/predict")


@celery_app.task(bind=True, max_retries=5)
def process_ml_request(self, data: dict):
    """
    Вызов синхронного AI API.
    При получении 429 - повторяем задачу с задержкой.
    """
    query = data.get('query', '')
    logger.info(f"Processing task for query: {query[:50]}...")
    
    try:
        response = requests.post(
            AI_API_URL,
            json={"query": query},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Task completed successfully")
            return {
                "status": "completed",
                "result": result.get("result", "No result"),
                "processing_time": result.get("processing_time", 0),
                "model": result.get("model", "unknown"),
                "task_id": self.request.id
            }
            
        elif response.status_code == 429:
            # AI API занят — повторяем задачу
            logger.warning(f"AI API busy (429), retrying in 3 seconds...")
            raise self.retry(countdown=3, max_retries=5)
            
        else:
            logger.error(f"AI API error: {response.status_code} - {response.text}")
            return {
                "status": "failed",
                "error": f"AI API error: {response.status_code}",
                "task_id": self.request.id
            }
            
    except requests.exceptions.Timeout:
        logger.error("AI API timeout, retrying...")
        raise self.retry(countdown=5, max_retries=3)
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to AI API, retrying...")
        raise self.retry(countdown=5, max_retries=5)
        
    except Retry:
        # Пробрасываем исключение Retry дальше
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "task_id": self.request.id
        }