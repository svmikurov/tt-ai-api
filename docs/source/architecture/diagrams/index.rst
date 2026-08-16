========================================
C4-Диаграммы
========================================

Уровень 1: Контекст
===================

.. code-block:: text

   .. image:: ../diagrams/context.png
      :alt: Context Diagram
      :width: 100%

.. .. code-block:: plantuml

.. code-block:: text

   @startuml
   !include <C4/C4_Container>

   Person(user, "Пользователь", "Отправляет запросы")
   System(backend, "Tech Task CHKPZ", "Бэкенд-сервис")
   System_Ext(ai_model, "ML Model", "Синхронная ML-модель")
   System_Ext(ai_api, "AI API", "Обёртка над ML-моделью")

   Rel(user, backend, "Отправляет запросы", "HTTPS")
   Rel(backend, ai_api, "Вызывает AI API", "HTTP")
   @enduml

Уровень 2: Контейнеры
=====================

.. code-block:: text

   .. image:: ../diagrams/containers.png
      :alt: Containers Diagram
      :width: 100%

.. .. code-block:: plantuml

.. code-block:: text

   @startuml
   !include <C4/C4_Container>

   Person(user, "Пользователь")

   Container(api, "API", "FastAPI", "Принимает запросы, отправляет задачи")
   Container(worker, "Worker", "Celery", "Обрабатывает задачи")
   Container(ai_api, "AI API", "FastAPI", "Синхронный ML-API")
   ContainerDb(redis, "Redis", "Брокер", "Очередь, статусы, результаты")
   ContainerDb(postgres, "PostgreSQL", "БД", "Профили, история")

   Rel(user, api, "Отправляет запросы", "HTTPS")
   Rel(api, redis, "Отправляет задачи", "TCP")
   Rel(redis, worker, "Передаёт задачи", "TCP")
   Rel(worker, ai_api, "Вызывает AI API", "HTTP")
   Rel(api, postgres, "Читает/пишет", "SQL")
   @enduml

Уровень 3: Компоненты API
=========================

.. code-block:: text

   .. image:: ../diagrams/components.png
      :alt: Components Diagram
      :width: 100%

.. .. code-block:: plantuml

.. code-block:: text

   @startuml
   !include <C4/C4_Component>

   Container(api, "API", "FastAPI")

   Component(entrypoints, "Entrypoints", "FastAPI", "Эндпоинты /predict, /result, /stream")
   Component(use_cases, "Use Cases", "Python", "Бизнес-логика")
   Component(producer, "TaskProducer", "Redis", "Отправка задач в очередь")
   Component(container, "DI Container", "Dependency Injector", "Внедрение зависимостей")

   Rel(entrypoints, use_cases, "Вызывает")
   Rel(use_cases, producer, "Использует")
   Rel(container, producer, "Внедряет")
   @enduml