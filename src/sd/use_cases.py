"""Use cases."""

from typing import Any

from .abstract import AbstractTaskProducer


class SendQuestionUseCase:
    """Use case for send question."""

    def __init__(
        self,
        task_producer: AbstractTaskProducer,
    ) -> None:
        self._task_produser = task_producer

    def execute(self, query: str) -> dict[str, Any]:
        """Send question."""
        task_id = self._task_produser.send_task(query)
        return {
            'task_id': task_id,
            'status': 'queued',
            'message': 'Task sent to ML worker',
        }


class GetResultUseCase:
    """Use Case для получения результата."""

    def __init__(self, task_producer: AbstractTaskProducer):
        self.task_producer = task_producer

    def execute(self, task_id: str) -> dict:
        """Get result."""
        status = self.task_producer.get_status(task_id)

        if status == 'completed':
            result = self.task_producer.get_result(task_id)
            return {
                'task_id': task_id,
                'status': 'completed',
                'result': result,
            }
        elif status == 'not_found':
            return {
                'task_id': task_id,
                'status': 'not_found',
                'message': 'Task not found',
            }
        else:
            return {
                'task_id': task_id,
                'status': 'pending',
                'message': 'Task is still processing',
            }
