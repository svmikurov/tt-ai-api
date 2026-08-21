========================================
API Документация (OpenAPI)
========================================

Документация доступна в Swagger UI:

**Swagger UI:** http://localhost:8000/docs

**ReDoc:** http://localhost:8000/redoc

**OpenAPI файл:** `./openapi.yaml`

Основные эндпоинты
==================

.. list-table:: Эндпоинты
   :header-rows: 1
   :widths: 20 30 20

   * - Эндпоинт
     - Метод
     - Описание
   * - `/predict`
     - POST
     - Отправка запроса на предсказание
   * - `/result/{task_id}`
     - GET
     - Получение результата (polling)
   * - `/stream/{task_id}`
     - GET (SSE)
     - Real-time результат
   * - `/health`
     - GET
     - Проверка состояния
   * - `/db-check`
     - GET
     - Проверка БД
   * - `/redis-check`
     - GET
     - Проверка Redis

Пример запроса
==============

.. code-block:: bash

   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"query": "Привет, нейросеть!"}'

Пример ответа
=============

.. code-block:: json

   {
     "task_id": "abc-123",
     "status": "queued",
     "message": "Task sent to ML worker"
   }