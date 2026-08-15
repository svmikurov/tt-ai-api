"""Services."""

from typing import Self

import aioredis


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
