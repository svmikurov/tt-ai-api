# docs/development/testing.rst
========================================
Тестирование
========================================

Структура тестов
================

::

   tests/
   ├── unit/              # Модульные тесты
   │   ├── test_use_cases.py
   │   └── test_broker.py
   ├── integration/       # Интеграционные тесты
   │   ├── test_api.py
   │   └── test_worker.py
   └── e2e/               # Сквозные тесты
       └── test_full_cycle.py

Запуск тестов
=============

.. code-block:: bash

   # Все тесты
   pytest

   # Только unit-тесты
   pytest tests/unit

   # Только интеграционные
   pytest tests/integration

   # С coverage
   pytest --cov=src/sd --cov-report=html

   # С параллельным запуском
   pytest -n auto

Запуск тестов в Docker
======================

.. code-block:: bash

   docker compose run --rm api pytest

   docker compose run --rm worker pytest

Написание тестов
================

.. code-block:: python

   # tests/unit/test_use_cases.py
   import pytest
   from unittest.mock import Mock
   from sd.api.use_cases import SendQuestionUseCase

   def test_send_question():
       # Arrange
       mock_producer = Mock()
       mock_producer.send_task.return_value = "task-123"
       use_case = SendQuestionUseCase(mock_producer)

       # Act
       result = use_case.execute("Hello")

       # Assert
       assert result["task_id"] == "task-123"
       assert result["status"] == "queued"