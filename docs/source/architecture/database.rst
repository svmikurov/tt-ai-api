========================================
Схема базы данных
========================================

PostgreSQL
==========

.. code-block:: text

  .. image:: ../diagrams/database.png
    :alt: ER-диаграмма
    :width: 100%

.. .. code-block:: plantuml

.. code-block:: text

   @startuml
   !include <C4/C4_Container>

   entity "users" {
     * id : UUID <<PK>>
     --
     * email : VARCHAR(255) <<UNIQUE>>
     * name : VARCHAR(100)
     * created_at : TIMESTAMP
     * updated_at : TIMESTAMP
   }

   entity "messages" {
     * id : UUID <<PK>>
     --
     * user_id : UUID <<FK>>
     * role : VARCHAR(20)  -- user / assistant
     * content : TEXT
     * task_id : UUID
     * created_at : TIMESTAMP
   }

   entity "sessions" {
     * id : UUID <<PK>>
     --
     * user_id : UUID <<FK>>
     * token : VARCHAR(255)
     * expires_at : TIMESTAMP
     * created_at : TIMESTAMP
   }

   users ||--o{ messages : "has"
   users ||--o{ sessions : "has"
   @enduml

Redis
=====

Хранение задач и статусов:

.. list-table:: Redis ключи
   :header-rows: 1
   :widths: 30 30 30

   * - Ключ
     - Тип
     - Описание
   * - `tasks`
     - List
     - Очередь задач (JSON)
   * - `status:{task_id}`
     - String
     - Статус задачи (queued/processing/completed)
   * - `result:{task_id}`
     - String
     - Результат задачи (JSON)