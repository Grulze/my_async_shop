from logging import getLogger, basicConfig, DEBUG, ERROR, StreamHandler,  FileHandler

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from router import router, crud_router
from database import create_table
from redis_conf import redis


logger = getLogger()
terminal_handler = StreamHandler()
terminal_handler.setLevel(ERROR)
file_handler = FileHandler(filename="logs.log", mode="w")
file_handler.setLevel(DEBUG)

basicConfig(
    level=DEBUG,
    format="%(asctime)s : %(name)s : %(levelname)s : %(message)s",
    handlers=[file_handler, terminal_handler]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start service...")
    logger.info("Connection to redis")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Connection to database")
    await create_table()
    logger.info("Service is ready to work")
    yield
    logger.info("Shut down service...")


my_shop = FastAPI(lifespan=lifespan)
my_shop.include_router(router)
my_shop.include_router(crud_router)
