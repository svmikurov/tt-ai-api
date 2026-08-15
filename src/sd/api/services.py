"""Services."""

import json
from enum import Enum
from typing import Self

import aio_pika
import aioredis


class QueueEnum(str, Enum):
    """Queue name enumeraion."""

    TASK_QUEUE = 'task_queue'


class RedisService:
    """Service for Redis."""

    def __init__(self, url: str) -> None:
        self._url = url
        self._redis: aioredis.Redis | None = None

    async def connect(self) -> Self:
        """Connect to Redis."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self._url,
                decode_responses=True,
            )
        return self

    async def close(self) -> None:
        """Close Redis connection."""
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
        """Save value with TTL."""
        return await self.client.setex(key, ttl, value)

    async def get(self, key: str) -> str | None:
        """Get value by key."""
        return await self.client.get(key)

    async def publish(self, channel: str, message: str) -> int:
        """Publish message to channel."""
        return await self.client.publish(channel, message)

    def pubsub(self):
        """Create pubsub instance."""
        return self.client.pubsub()


class RabbitMQService:
    """Service for RabbitMQ."""

    def __init__(self, url: str) -> None:  # ✅ Добавили url
        self._url = url
        self._connection: aio_pika.Connection | None = None
        self._channel: aio_pika.Channel | None = None
        self._queue_name = QueueEnum.TASK_QUEUE

    async def connect(self) -> Self:
        """Connect to RabbitMQ."""
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self._queue_name, durable=True)
        return self

    async def close(self) -> None:
        """Close connection."""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
            self._channel = None

    @property
    def connection(self) -> aio_pika.Connection:
        """Connection."""
        if self._connection is None:
            raise RuntimeError(
                'Connection not initialized. Call connect() first.'
            )
        return self._connection

    @property
    def channel(self) -> aio_pika.Channel:
        """Channel."""
        if self._channel is None:
            raise RuntimeError(
                'Channel not initialized. Call connect() first.'
            )
        return self._channel

    async def publish(self, message: str, correlation_id: str) -> None:
        """Publish message to queue."""
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                correlation_id=correlation_id,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._queue_name,
        )

    async def get_queue(self):
        """Get queue instance."""
        return await self.channel.get_queue(self._queue_name)

    async def publish_task(self, correlation_id: str, task_data: str) -> None:
        """Publish task to queue."""
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
        """Consume one message from queue."""
        queue = await self.get_queue()
        try:
            return await queue.get(timeout=timeout)
        except aio_pika.exceptions.QueueEmpty:
            return None

    async def acknowledge(self, message: aio_pika.Message) -> None:
        """Acknowledge message."""
        await message.ack()
