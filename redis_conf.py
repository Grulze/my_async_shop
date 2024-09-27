from fastapi_cache import FastAPICache
from redis import asyncio as aioredis

from logging import getLogger

logger = getLogger(__name__)

redis = aioredis.from_url("redis://redis:6379")


async def check_cache_memory():
    keys = await redis.keys()
    logger.debug("Checking the quantity of keys in cache")
    if len(keys) > 100:
        await redis.delete(*keys[:5])
        logger.debug("Deleting 5 entries from the cache")


async def clear_cache_on_update(cache_id: int | None = None):
    logger.debug("Deleting data from the cache with a prefix 'all_items'")
    await FastAPICache.clear(namespace="all_items")
    if cache_id:
        logger.debug("Deleting data from the cache with a prefix 'item-%s'", cache_id)
        await FastAPICache.clear(namespace=f"item-{cache_id}")
