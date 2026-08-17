Бэкенд для сервиса взаимодействия с ML-моделью
==============================================

Кейс
----

«Нужно создать **бэкенд для сервиса взаимодействия с ML-моделью**.
API модели уже настроено и готово (работает синхронно, 1 вопрос – 1 ответ, остальные отбрасываются). 
Нужно обеспечить работу нескольких сотен пользователей в реальном времени.
Дизайн и фронтенд предоставляются.».


Документация
------------

Сформировать и открыть документацию в браузере:

- с использованием ``Docker``

.. code-block:: bash

   make docs-docker-run

.. code-block:: bash

   make docs-docker-stop

- в виртуальном окружении ``python``

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.docs.txt
   make -C docs html
   xdg-open docs/build/html/index.html 2>/dev/null || true
