Технологии передачи данных
==========================

HTTP
----

REST API работает по классической схеме HTTP:

- Клиент отправляет запрос (GET, POST, PUT, DELETE и т.д.)

 .. code-block:: text

    GET users/{id}

- Сервер обрабатывает и отправляет ответ
- Соединение закрывается (или остается в пуле, но логически это отдельная транзакция)



WebSocket
---------

WebSocket использует HTTP для установки соединения, после сервер отвечает готовностью
с переключением на WS протокол.

Это называется рукопожатие (handshake):

- Клиент шлет HTTP-запрос с заголовками

- Соединение остается HTTP-соединением (не переключается на другой протокол).

- Сервер просто долго держит это соединение открытым и периодически шлет кусочки данных (чанками) в формате data: ...\n\n.

  .. code-block:: text

     GET ai/generate

     Connection: Upgrade
     Upgrade: websocket

- Сервер отвечает статусом 101 Switching Protocols.
- После этого соединение переключается на протокол WebSocket, который работает поверх TCP,
  но уже НЕ поверх HTTP.
- Сервер отпраляет - фреймы

Запрос клиента
~~~~~~~~~~~~~~

GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket      ← Ключевой заголовок
Connection: Upgrade     ← Ключевой заголовок
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Origin: http://example.com

Ответ сервера:
~~~~~~~~~~~~~~

HTTP/1.1 101 Switching Protocols   ← СТАТУС 101!
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

Фрейм
~~~~~

.. code-block:: text

   [0x81 0x05 0x48 0x65 0x6C 0x6C 0x6F]  ← Текстовый фрейм "Hello"
   [0x82 0x04 0x01 0x02 0x03 0x04]       ← Бинарный фрейм

WebSocket не накладывает ограничений на формат данных:

.. code-block:: javascript

    // Можно отправлять что угодно
    ws.send(JSON.stringify({ type: 'message', data: 'Hello' }));
    ws.send('plain text');
    ws.send(new Uint8Array([1, 2, 3, 4]));
    ws.send(Buffer.from('binary data'));



SSE
---

`Server-Sent Events Specification <https://html.spec.whatwg.org/multipage/server-sent-events.html>`_

- Клиент отправляет обычный HTTP-запрос (например, GET /events).

- Сервер отвечает статусом 200 OK и специальным заголовком Content-Type: text/event-stream.

  Chunked Transfer Encoding

Запрос клиента
~~~~~~~~~~~~~~

.. code-block:: text

   GET /events HTTP/1.1
   Host: example.com
   Accept: text/event-stream

Ответ сервера
~~~~~~~~~~~~~

.. code-block:: text

    Пакет №1 (установка соединения и отправка заголовков): 

    HTTP/1.1 200 OK\r\n  # Версия протокола | Код статуса | Пояснение (стартовая строка)
    Content-Type: text/event-stream\r\n  # критически важен, без него браузер не поймет, что это SSE
    Cache-Control: no-cache\r\n  # чтобы прокси не сохраняли ответ
    Connection: keep-alive\r\n  # явно указывает держать соединение открытым
    X-Accel-Buffering: no\r\n  # отключает буферизацию на уровне Nginx (чтобы данные доходили сразу)
    \r\n                       # пустая строка отделяет заголовки от тела

    Пакет №2 (первый чанк с данными, отправлен сразу после заголовков)
    или ": heartbeat\n\n":

    36\r\n                     # размер первого чанка в hex  
    data: Событие 1\r\n
    data: {"user": "Alice", "action": "login", "time": 1744567890}
    \r\n                       # конец чанка

    Пакет №3 (второй чанк, отправлен через 5 секунд):

    15\r\n                     # размер второго чанка в hex  
    data: {\r\n
    data:   "user": "Alice",\r\n
    data:   "action": "login",\r\n
    data:   "time": 1744567890\r\n
    data: }\r\n
    \r\n                       # конец чанка

    Пакет №4 (закрытие соединения):

    0\r\n
    \r\n
    [TCP FIN]                 # закрываем соединение

Поля SSE
~~~~~~~~

.. list-table:: Поля Server-Sent Events (SSE)
   :header-rows: 1
   :widths: 15 50 35
   :class: longtable

   * - Поле
     - Назначение
     - Где используется
   * - ``data``
     - Данные события (любой текст/JSON)
     - На клиенте через ``event.data``
   * - ``event``
     - Тип события (для разных обработчиков)
     - На клиенте через ``addEventListener``
   * - ``id``
     - Идентификатор события (для восстановления)
     - На клиенте через ``event.lastEventId``, в запросе как ``Last-Event-ID``
   * - ``retry``
     - Время переподключения (в мс)
     - Автоматически применяется браузером
   * - ``:``
     - Комментарий (игнорируется)
     - Для отладки