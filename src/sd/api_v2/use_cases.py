"""Use cases."""

import json
import time
import uuid
from typing import Any, AsyncGenerator

from .abstract import AbstractResultStorage, AbstractTaskProducer
from .enums import SSEvent


class TaskUseCase:
    """Task use case."""

    def __init__(
        self,
        task_producer: AbstractTaskProducer,
        result_storage: AbstractResultStorage,
    ) -> None:
        self._task_producer = task_producer
        self._result_storage = result_storage

    async def execute(
        self,
        query: str,
    ) -> AsyncGenerator[str, None]:
        """Execute use case."""
        # The task has an identifier for retrieval and tracking.
        task_id = str(uuid.uuid4())

        # The task is sent to the queue for execution.
        await self._task_producer.send_task(task_id, query)

        # The server sends the task identifier in the first chunk.
        yield json.dumps(
            {
                'event': SSEvent.CREATED.value,
                'task_id': task_id,
                'timestamp': time.time(),
            },
        )

        # Only the task comleted event is sent to the client.
        async for event in self._result_storage.listen(task_id):
            if event.has_result:
                yield event.dump_to_json()
