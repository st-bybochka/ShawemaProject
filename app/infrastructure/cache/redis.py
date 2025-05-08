import aioredis
from aioredis import Redis

class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Redis | None = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get_redis(self) -> Redis:
        if not self.redis:
            await self.connect()
        return self.redis