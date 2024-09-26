from typing import List

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend

from query_db import get_items_db
from router import router
from database import create_table
from schema import GetItems, Pagination

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print("Connection...")
    await create_table()
    yield
    print("Shut down...")


my_shop = FastAPI(lifespan=lifespan)
my_shop.include_router(router)


@my_shop.get("/items", tags=["All items"])
@cache(50, namespace="all_items")
async def get_items(pagination: Pagination = Depends()) -> List[GetItems]:
    """
    Returns all items from database with pagination.
    :param pagination:
    :return: List[GetItems]
    """
    return await get_items_db(lim=pagination.limit, page=pagination.page)
