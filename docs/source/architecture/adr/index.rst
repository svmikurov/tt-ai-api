Architecture Decision Records
=============================

.. toctree::
   :maxdepth: 2

   conventions/index
   adr-XXX-template


.. toctree::
   :maxdepth: 2
   :caption: Список решений

   adr-001-use-fastapi
   adr-002-use-celery
   adr-003-use-sse
   adr-004-use-docker
   adr-005-use-redis
   adr-006-clean-architecture
   adr-007-api-gateway


Статусы решений


.. list-table::
   :header-rows: 1
   :widths: 10 40 15 15

   * - №
     - Решение
     - Статус
     - Дата
   * - :doc:`ADR-001 <adr-001-use-fastapi>`
     - Использование FastAPI
     - Принято
     - 2026-08-15
   * - :doc:`ADR-002 <adr-002-use-celery>`
     - Использование Celery
     - Принято
     - 2026-08-15
   * - :doc:`ADR-003 <adr-003-use-sse>`
     - Использование SSE для Real-Time уведомлений
     - Принято
     - 2026-08-16
   * - :doc:`ADR-004 <adr-004-use-docker>`
     - Использование Docker и Docker Compose
     - Принято
     - 2026-08-16
   * - :doc:`ADR-005 <adr-005-use-redis>`
     - Использование Redis как брокера сообщений
     - Принято
     - 2026-08-16
   * - :doc:`ADR-006 <adr-006-clean-architecture>`
     - Чистая архитектура (Clean Architecture)
     - Принято
     - 2026-08-16
   * - :doc:`ADR-007 <adr-007-api-gateway>`
     - Вынесение аутентификации на API Gateway
     - Принято
     - 2026-08-16
  