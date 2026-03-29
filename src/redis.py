import redis.asyncio as redis
from src.config import settings


class RedisClient:
    def __init__(self):
        self.client: redis.Redis | None = None

    async def connect(self):
        self.client = await redis.from_url(
            settings.redis.url, encoding="UTF-8", decode_responses=True
        )

    async def disconnect(self):
        if self.client:
            await self.client.close()

    async def add_to_blacklist(self, token: str, expire_seconds: int):
        """Add token to blacklist with expiration"""
        if self.client:
            await self.client.setex(f"blacklist:{token}", expire_seconds, "revoked")

    async def is_blacklisted(self, token: str) -> bool:
        """Check if token is in blacklist"""
        if self.client:
            return await self.client.exists(f"blacklist:{token}") > 0
        return False


redis_client = RedisClient()
