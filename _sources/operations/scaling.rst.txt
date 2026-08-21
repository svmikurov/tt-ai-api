========================================
Масштабирование
========================================

Пороги масштабирования
=======================

.. list-table:: Условия масштабирования
   :header-rows: 1
   :widths: 30 20 20 20

   * - Компонент
     - Метрика
     - Порог
     - Действие
   * - **API**
     - RPS (запросов/сек)
     - > 200
     - Добавить экземпляр API
   * - **Worker**
     - Длина очереди (tasks)
     - > 100
     - Добавить воркера
   * - **Worker**
     - Время обработки
     - > 10 сек
     - Добавить воркера
   * - **AI API**
     - Ошибки 429
     - > 5%
     - Увеличить ресурсы
   * - **Redis**
     - Использование памяти
     - > 80%
     - Увеличить память
   * - **PostgreSQL**
     - Подключения
     - > 100
     - Увеличить пул соединений

Горизонтальное масштабирование
==============================

API
---

.. code-block:: bash

   docker compose up -d --scale api=3

Worker
------

.. code-block:: bash

   docker compose up -d --scale worker=5

Вертикальное масштабирование
============================

Redis
-----

.. code-block:: yaml

   redis:
     image: redis:7-alpine
     command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru

PostgreSQL
----------

.. code-block:: yaml

   db:
     image: postgres:15-alpine
     environment:
       - POSTGRES_SHARED_BUFFERS=512MB

Автоматическое масштабирование
==============================

Для Kubernetes можно использовать HPA (Horizontal Pod Autoscaler):

.. code-block:: yaml

   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: worker-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: worker
     minReplicas: 2
     maxReplicas: 10
     metrics:
       - type: Resource
         resource:
           name: cpu
           target:
             averageUtilization: 70