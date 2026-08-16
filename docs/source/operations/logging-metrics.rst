========================================
Логи и Метрики
========================================

Логи
====

Логи Docker Compose
-------------------

.. code-block:: bash

   # Все логи
   docker compose logs -f

   # Логи API
   docker compose logs -f api

   # Логи Worker
   docker compose logs -f worker

   # Логи AI API
   docker compose logs -f ai-api

Структура логов
---------------

.. code-block::

   2026-08-16 14:30:25 - sd.api.entrypoints - INFO - Request received: /predict
   2026-08-16 14:30:25 - sd.worker.tasks - INFO - Processing task: abc-123...
   2026-08-16 14:30:28 - sd.worker.tasks - INFO - Task abc-123 completed

Метрики
=======

Доступные метрики (AI API)
--------------------------

.. code-block:: bash

   curl http://localhost:8001/metrics

.. code-block:: json

   {
     "model": "sync-ai-model",
     "busy": false,
     "max_concurrent_requests": 1
   }

Метрики Redis
-------------

.. code-block:: bash

   docker compose exec redis redis-cli INFO

Пороговые значения
------------------

.. list-table:: Метрики для мониторинга
   :header-rows: 1
   :widths: 30 20 40

   * - Метрика
     - Порог
     - Действие
   * - Длина очереди
     - > 100
     - Добавить воркеров
   * - Время обработки
     - > 10 сек
     - Проверить AI API
   * - Ошибки (429)
     - > 10%
     - Проверить AI API