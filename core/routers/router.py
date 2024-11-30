from typing import List
from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from core.db.query_db import add_items_db, delete_items_db, get_items_db, update_items_db
from core.schemas.schema import AddItems, GetItems, PutItems, PatchItems, Pagination
from core.custom_exceptions import invalid_id

from core.cache.redis_conf import check_cache_memory, clear_cache_on_update

logger = getLogger(__name__)

crud_router = APIRouter(prefix="/items", tags=["CRUD items"])
router = APIRouter(prefix="/items", tags=["All items"])


@router.get("")
async def get_all_items(pagination: Pagination = Depends()) -> List[GetItems]:
    """
    Return all items from database with pagination.
    :param pagination: class with information that used for pagination
    :return: List[GetItems]
    """
    logger.debug("Client requested items with pagination: limit - %s, page - %s",
                 pagination.limit, pagination.page)

    @cache(2, namespace="all_items")
    async def send_request_to_db():
        return await get_items_db(lim=pagination.limit, page=pagination.page)

    await check_cache_memory()
    return await send_request_to_db()


@crud_router.get("/{item_id}")
async def get_items(item_id: int) -> List[GetItems]:
    """
    Return the item by the specified id from database.
    :param item_id: id of item from database
    :return: List[GetItem]
    """
    logger.debug("Client requested item with item_id - %s", item_id)

    if type(item_id) != int or item_id < 1:
        invalid_id()

    @cache(2, namespace=f"item-{item_id}")
    async def send_request_to_db():
        return await get_items_db(item_id_db=item_id)

    await check_cache_memory()
    return await send_request_to_db()


@crud_router.post("", status_code=201)
async def new_items(item: AddItems = Depends()):
    """
    Add a new item to the database.
    :param item: class with information that needs to be added to database
    :return: str
    """
    logger.debug("Client requested to create new item")

    await clear_cache_on_update()
    await add_items_db(item)


@crud_router.put("/{item_id}", status_code=204)
async def update_items(item_id: int, data: PutItems = Depends()):
    """
    Update all information about the product with the specified id.
    :param item_id: id of item from database
    :param data: class with information that needs to be updated in database
    :return:
    """
    logger.debug("Client requested to update item with item_id - %s by method - PUT", item_id)

    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await update_items_db(item_id, data.dict())


@crud_router.patch("/{item_id}")
async def partial_update_items(item_id: int, data: PatchItems = Depends()) -> List[GetItems]:
    """
    Update partial information about the product with the specified id.
    :param item_id: id of item from database
    :param data: class with a piece of information that needs to be updated in database
    :return:
    """
    logger.debug("Client requested to update item with item_id - %s by method - PATCH", item_id)

    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await update_items_db(item_id, data.dict(exclude_none=True))
    return await get_items_db(item_id)


@crud_router.delete("/{item_id}", status_code=204)
async def delete_items(item_id: int):
    """
    Delete item with the passed id.
    :param item_id: id of item from database
    :return: str
    """
    logger.debug("Client requested to delete item with item_id - %s", item_id)

    if type(item_id) != int or item_id < 1:
        invalid_id()

    await clear_cache_on_update(item_id)
    await delete_items_db(item_id)
