"""
Redis client configuration and utilities
"""

import redis.asyncio as redis
import json
import logging
from typing import Any, Optional
from core.config import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper with async support"""

    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.settings = get_settings()

    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.from_url(
                self.settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            # Test connection
            await self.client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Disconnected from Redis")

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a key-value pair with optional TTL"""
        if not self.client:
            await self.connect()

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        if ttl:
            await self.client.setex(key, ttl, value)
        else:
            await self.client.set(key, value)

    async def get(self, key: str) -> Optional[Any]:
        """Get a value by key"""
        if not self.client:
            await self.connect()

        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def delete(self, key: str):
        """Delete a key"""
        if not self.client:
            await self.connect()

        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            await self.connect()

        return await self.client.exists(key)

    async def setex(self, key: str, ttl: int, value: Any):
        """Set key with expiration"""
        await self.set(key, value, ttl)

    async def publish(self, channel: str, message: Any):
        """Publish message to a channel"""
        if not self.client:
            await self.connect()

        if isinstance(message, (dict, list)):
            message = json.dumps(message)

        await self.client.publish(channel, message)

    async def subscribe(self, *channels):
        """Subscribe to channels"""
        if not self.client:
            await self.connect()

        pubsub = self.client.pubsub()
        await pubsub.subscribe(*channels)
        return pubsub


# Global Redis client instance
_redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """Get the global Redis client instance"""
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
    return _redis_client
