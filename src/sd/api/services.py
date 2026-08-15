"""Services."""

import json
import uuid
from typing import Self

import aio_pika
import aioredis


class RedisService:
    """Service for Redis operations."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._redis: aioredis.Redis | None = None

    async def connect(self) -> Self:
        """Establish connection to Redis."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self._url,
                decode_responses=True,
            )
        return self

    async def close(self) -> None:
        """Close Redis connection gracefully."""
        if self._redis is not None:
            await self._redis.close()
            self._redis = None

    @property
    def client(self) -> aioredis.Redis:
        """Redis client.

        Raises if not connected.
        """
        if self._redis is None:
            raise RuntimeError('Redis client not initialized.')
        return self._redis

    async def setex(self, key: str, ttl: int, value: str) -> str:
        """Store value with expiration time."""
        return await self.client.setex(key, ttl, value)

    async def get(self, key: str) -> str | None:
        """Retrieve value by key."""
        return await self.client.get(key)

    async def publish(self, channel: str, message: str) -> int:
        """Send message to a channel."""
        return await self.client.publish(channel, message)

    def pubsub(self):
        """Create pub/sub instance."""
        return self.client.pubsub()


class RabbitMQService:
    """Service for RabbitMQ messaging."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._connection: aio_pika.Connection | None = None
        self._channel: aio_pika.Channel | None = None
        self._queue_name = 'task_queue'

    async def connect(self) -> Self:
        """Establish connection to RabbitMQ."""
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self._queue_name, durable=True)
        return self

    async def close(self) -> None:
        """Close RabbitMQ connection."""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
            self._channel = None

    @property
    def connection(self) -> aio_pika.Connection:
        """RabbitMQ connection."""
        if self._connection is None:
            raise RuntimeError(
                'Connection not initialized. Call connect() first.'
            )
        return self._connection

    @property
    def channel(self) -> aio_pika.Channel:
        """RabbitMQ channel."""
        if self._channel is None:
            raise RuntimeError(
                'Channel not initialized. Call connect() first.'
            )
        return self._channel

    async def publish(self, message: str, correlation_id: str) -> None:
        """Send message to queue with correlation ID."""
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                correlation_id=correlation_id,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._queue_name,
        )

    async def get_queue(self):
        """Retrieve queue instance."""
        return await self.channel.get_queue(self._queue_name)

    async def publish_task(self, correlation_id: str, task_data: str) -> None:
        """Publish task message to queue."""
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(
                    {'correlation_id': correlation_id, 'task_data': task_data}
                ).encode(),
                correlation_id=correlation_id,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._queue_name,
        )

    async def consume_one(self, timeout: float = 5.0):
        """Fetch single message from queue."""
        queue = await self.get_queue()
        try:
            return await queue.get(timeout=timeout)
        except aio_pika.exceptions.QueueEmpty:
            return None

    async def acknowledge(self, message: aio_pika.Message) -> None:
        """Acknowledge processed message."""
        await message.ack()


class TaskService:
    """Task management service."""

    def __init__(
        self,
        redis_service: RedisService,
        rabbit_service: RabbitMQService,
    ):
        self._redis = redis_service
        self._rabbit = rabbit_service

    async def create_task(self, task_data: str) -> str:
        """Create a task and send it to the queue."""
        correlation_id = str(uuid.uuid4())
        await self._rabbit.publish_task(correlation_id, task_data)
        return correlation_id

    async def get_result(self, correlation_id: str) -> str | None:
        """Get task result from Redis."""
        return await self._redis.get(f'result:{correlation_id}')

    async def save_result(self, correlation_id: str, result: str):
        """Save result to Redis with a 5-minute TTL."""
        await self._redis.setex(
            f'result:{correlation_id}',
            300,
            json.dumps(
                {
                    'status': 'completed',
                    'result': result,
                    'correlation_id': correlation_id,
                }
            ),
        )
        # Notify via Pub/Sub
        await self._redis.publish(f'result:{correlation_id}', 'done')
