========================================
CI/CD Pipeline
========================================

Общая схема
===========

.. code-block::

   Developer → Git → GitHub Actions → Docker Registry → Production

Этапы CI
========

1. **Lint** — проверка стиля кода
2. **Tests** — запуск тестов
3. **Build** — сборка Docker-образов
4. **Push** — загрузка в Docker Registry

Этапы CD
========

1. **Deploy to Staging** — развёртывание на тестовое окружение
2. **Smoke Tests** — минимальная проверка
3. **Deploy to Production** — развёртывание на продакшен
4. **Monitor** — проверка метрик

GitHub Actions
==============

.. code-block:: yaml

   name: CI/CD

   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]

   jobs:
     build-and-test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Install dependencies
           run: pip install -r requirements.system.txt
         - name: Run tests
           run: pytest
         - name: Build Docker images
           run: docker compose build

     deploy:
       needs: build-and-test
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       steps:
         - name: Deploy to production
           run: ./scripts/deploy.sh