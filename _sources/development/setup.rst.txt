========================================
Инструкция по запуску
========================================

Требования
==========

- Docker 24.0+
- Docker Compose 2.0+
- Python 3.12+ (для локальной разработки)

Быстрый старт (Docker Compose)
==============================

.. code-block:: bash

   # Клонировать репозиторий
   git clone https://github.com/org/tech-task-chkpz.git
   cd tech-task-chkpz

   # Скопировать переменные окружения
   cp .env.example .env

   # Запустить всё
   docker compose up --build

Локальная разработка
====================

.. code-block:: bash

   # Создать виртуальное окружение
   python -m venv venv
   source venv/bin/activate

   # Установить зависимости
   pip install -r requirements.system.txt

   # Запустить API
   uvicorn sd.api.application:app --reload

   # Запустить Worker (отдельно)
   celery -A sd.worker.tasks worker --loglevel=info

   # Запустить AI API (отдельно)
   uvicorn sd.ai_api.ai_api:app --port 8001 --reload

Переменные окружения (.env)
===========================

.. list-table:: Переменные окружения
   :header-rows: 1
   :widths: 30 20 40

   * - Переменная
     - По умолчанию
     - Описание
   * - `DATABASE_URL`
     - `postgresql://user:password@db:5432/demo`
     - Подключение к PostgreSQL
   * - `REDIS_URL`
     - `redis://redis:6379/0`
     - Подключение к Redis
   * - `AI_API_URL`
     - `http://ai-api:8001/predict`
     - URL AI API
   * - `BROKER_TYPE`
     - `redis`
     - Тип брокера (redis/kafka)