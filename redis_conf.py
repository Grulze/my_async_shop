from redis import asyncio as aioredis


redis = aioredis.from_url("redis://localhost:6379")


async def check_cache_memory():
    keys = await redis.keys()
    if len(keys) > 100:
        await redis.delete(*keys[:5])
